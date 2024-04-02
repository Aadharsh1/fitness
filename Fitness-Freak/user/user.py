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

    query = users_ref.where('userID', '==', user_id).limit(1)
    user_docs = query.stream()
    # Check if any document is found
    for user_doc in user_docs:
        user_data = user_doc.to_dict()
        return jsonify(user_data), 200


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
        new_lpoints = current_lpoints + int(additional_lpoints)
        user_doc_ref = users_ref.document(user_doc.id)
        user_doc_ref.update({'lpoints': new_lpoints})

    if user_found:
        return jsonify({'newlpoints': new_lpoints}), 200
    else:
        return jsonify({"error": "User not found"}), 404
    

@app.route('/update_user_profile/<user_id>', methods=['PUT'])
def update_user_profile(user_id):
    # Extract the updated profile data from the request
    updated_data = request.json
    print(user_id)

    try:
        query = users_ref.where('userID', '==', user_id).limit(1)
        user_docs = query.stream()
        for user_doc in user_docs:
            user_doc_ref = users_ref.document(user_doc.id)
            user_doc_ref.update(updated_data)
        return jsonify({"message": "User profile updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

