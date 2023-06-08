"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():


    members = jackson_family.get_all_members()
    if 'error' in members:
        return jsonify(members), 404
    response_body = members
    return jsonify(response_body), 200


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member_by_id(member_id):
    member = jackson_family.get_member(member_id)
    if 'error' in member:
        return jsonify(member), 404
    response_body = {
        "id": member['id'],
        "first_name": member['first_name'],
        "age": member['age'],
        "lucky_numbers": member['lucky_numbers']
    }
    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def add_new_member():
    new_member = request.json
    if 'first_name' not in new_member or 'age' not in new_member or 'lucky_numbers' not in new_member:
        return jsonify({'error': 'keys missing, please be sure to send "first_name", "age" and "lucky_numbers"'}), 400
    if 'id' not in new_member:
        new_member['id'] = jackson_family._generateId()
    jackson_family.add_member(new_member)
    return jsonify({}), 200


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member_by_id(member_id):
    member = jackson_family.delete_member(member_id)
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    return jsonify({'done': True}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
