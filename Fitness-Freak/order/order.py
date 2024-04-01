import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, jsonify, request
import json
import datetime
# from notification import test_order

cred = credentials.Certificate("ordersdb_serviceAccountKey.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route('/create_order', methods=['POST'])
def create_order():
    try:
        user_id = request.form['userId']
        data1 = request.json
        lpoints_used = int(data1.get('discount_amount', 0))
        cart = data1.get('cart', None)
        email = data1.get('email', None)
        
        # cart_json_string = request.form['cart']
        # cart = json.loads(cart_json_string)
        current_date = datetime.datetime.now().date()
        formatted_date = current_date.strftime("%Y-%m-%d")
        # print(lpoints_used, cart, formatted_date)
        # return lpoints_used
        order_data = {
            "user_id": user_id,
            "items": [],
            "date_created": formatted_date,
            "price_before_discount": 0, 
            "lpoints_used": lpoints_used,
            'email': email
        }
        # # Add each item in the cart to the order data

        for item in cart:
            order_data['price_before_discount'] += item['price'] * item['quantity']
            order_data['items'].append({
                "title": item['title'],
                "price": item['price'],
                "quantity": item['quantity'],
                "availability": item['availability'],
                "product_id": item['id']
            })

        # Calculate final total price after applying discount
        final_total_price = order_data['price_before_discount'] - (lpoints_used/100)
        order_data['final_total_price'] = final_total_price  # Add final total price to order data

        db = firestore.client()
        orders_ref = db.collection("ordersdb")
        orders_ref.add(order_data)
        # order_id = new_order_ref.id

        print('order created')
        return jsonify(order_data), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port = 5010)
