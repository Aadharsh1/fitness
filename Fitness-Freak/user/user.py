import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, jsonify, request

app = Flask(__name__)
cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred)

from flask_cors import CORS
CORS(app)

db = firestore.client()
users_ref = db.collection('users')

@app.route('/users', methods=['GET'])
def read():
    all_users = []
    for doc in users_ref.stream():
        user_data = doc.to_dict()
        user_data['id'] = doc.id
        all_users.append(user_data)
    return jsonify(all_users), 200

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):

    #cannot use this method anymore since userID is inside the user table
    # user_doc = users_ref.document(user_id).get()
    # if user_doc.exists:
    #     user_data = user_doc.to_dict()
    #     return jsonify(user_data), 200
    # else:
    #     return jsonify({"error": "User not found"}), 404
    query = users_ref.where('userID', '==', user_id).limit(1)
    user_docs = query.stream()
    # Check if any document is found
    for user_doc in user_docs:
        user_data = user_doc.to_dict()
        return jsonify(user_data), 200
    
    # # If no matching document is found, return an error response
    # return jsonify({"error": "User not found"}), 404

@app.route('/user_lpoints/<user_id>', methods=['GET'])
def get_user_lpoints(user_id):

    query = users_ref.where('userID', '==', user_id).limit(1)
    user_docs = query.stream()
    # Check if any document is found
    for user_doc in user_docs:
        user_data = user_doc.to_dict()
        return jsonify(user_data.get('lpoints')), 200
    
@app.route('/update_user_lpoints/<user_id>', methods=['PUT'])
def update_user_lpoints(user_id):
    additional_lpoints = request.json.get('lpoints')
    query = users_ref.where('userID', '==', user_id).limit(1)
    user_docs = query.stream()
    user_found = False
    for user_doc in user_docs:
        user_found = True
        user_data = user_doc.to_dict()
        current_lpoints = user_data.get('lpoints', 0)
        # print(current_lpoints, type(current_lpoints))
        # print(additional_lpoints, type(additional_lpoints))
        new_lpoints = current_lpoints + int(additional_lpoints)
        user_doc_ref = users_ref.document(user_doc.id)
        user_doc_ref.update({'lpoints': new_lpoints})

    if user_found:
        return jsonify({'newlpoints': new_lpoints}), 200
    else:
        return jsonify({"error": "User not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

