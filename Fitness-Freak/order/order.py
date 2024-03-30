import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, jsonify, request
# from notification import test_order

cred = credentials.Certificate("ordersdb_serviceAccountKey.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route('/create_order', methods=['POST'])
def create_order():
    try:
        discount_amount = request.form['discountAmount']
        cart = request.form['cart']
        print(discount_amount, cart)
        # Add order data to Firestore
        # db = firestore.client()
        # db.collection("ordersdb").add(order_data)

        
        return jsonify({"message": "Order added successfully"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port = 5010)
