import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, jsonify, request
<<<<<<< HEAD
# from notification import test_order
=======
from notification import test_order
>>>>>>> 0039ffd388e2332764047a15a9178b5aff32dc78

cred = credentials.Certificate("ordersdb_serviceAccountKey.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route('/create_order', methods=['POST'])
def create_order():
    try:
        order_data = request.json
        
        # Add order data to Firestore
        db = firestore.client()
        db.collection("ordersdb").add(order_data)

        
        return jsonify({"message": "Order added successfully"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
