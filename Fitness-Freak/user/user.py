import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, jsonify


cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred)

from flask_cors import CORS
app = Flask(__name__)
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
        return jsonify(user_data.get('lpoints')), 200

if __name__ == '__main__':
    app.run(debug=True, port=5003)

