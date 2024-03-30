import requests
from flask import Flask, jsonify, render_template, request
import stripe
from flask_cors import CORS
import json 

stripe.api_key = 'sk_test_51OuT5rDip6VoQJfrbgZM63TUyy4WeWzG2JCjJmMXwAMmJ0eSLL3LkZtlUKrUjCrjdQr6dEUD4lac2MQonS304vtL00cbcZkXtH'
endpoint_secret = 'whsec_6c9ba7e888b57c5367963e9546d5c1df0a9d59c8ecdacf687b010f0938d52e03'


app = Flask(__name__)
CORS(app)
USER_MICROSERVICE_URL = 'http://127.0.0.1:5003'
PAYMENT_MICROSERVICE_URL = 'http://127.0.0.1:5007'


userId = 'awrWt0Rv0hRkwmXerlHKHr9BoJt1'
ORDER_MICROSERVICE_URL = 'http://127.0.0.1:5010'

tcart = None
tpoints = None
tuid = None

#dk whether need
# @app.route('/process_order/<user_Id>', methods=['GET'])
# def process_order(user_id):
#     # Retrieve user data from user microservice
#     user_response = requests.get(f'{USER_MICROSERVICE_URL}/users/{user_id}')
#     if user_response.status_code == 200:
#         user_data = user_response.json()

#         # Process order and payment
#         # For simplicity, we'll just return the user data here
#         return jsonify(user_data)
#     else:
#         return jsonify({"error": "User not found"}), 404


@app.route('/get_payment_status', methods=['GET'])
def get_payment_status():
    user_response = requests.get(f'{USER_MICROSERVICE_URL}/users/{userId}')
    if user_response.status_code != 200:
        return jsonify({"error": "User not found"}), 404
    
    user_data = user_response.json()
    cart = user_data.get('cart', [])
    maxLPoints = user_data.get('lpoints')
    total_amount_before_discount = sum(item['price'] * item['quantity'] for item in cart)
    maximum_total = total_amount_before_discount * 15
    if maxLPoints <  maximum_total:
        maximum_total = maxLPoints
    return render_template('user_data.html', cart=cart, maxLPoints=maxLPoints, total_amount_before_discount=total_amount_before_discount, maximum_total = maximum_total)


@app.route('/get_user_points/<uid>', methods=['GET'])
def get_user_points(uid):
    user_response = requests.get(f'{USER_MICROSERVICE_URL}/user_lpoints/{uid}')
    if user_response.status_code == 200:
        return jsonify(user_response.json()), 200


@app.route('/create_checkout_session', methods=['POST'])
def create_checkout_session():
    try:
        discount_amount = request.form['discountAmount']
        cart = request.form['cart']
        tpoints = discount_amount
        tcart = cart
        
        payment_response = requests.get(f'{PAYMENT_MICROSERVICE_URL}/get_payment_url',json={
        'discount_amount': discount_amount,
        'cart': json.loads(cart)  
    })
        
        if payment_response.status_code == 200:
            # Extract the payment URL from the response and send it back
            payment_url = payment_response.text
            return payment_url, 200
        else:
            return jsonify({"error": "Failed to get payment URL"}), payment_response.status_code
        
        # Get user data
        user_response = requests.get(f'{USER_MICROSERVICE_URL}/users/{user_id}')
        if user_response.status_code != 200:
            return jsonify({"error": "User not found"}), 404

        # Get payment data (jj's part)
        data = requests.get_json()
        # discount_amount = data.get('discountAmount')
        # cart_items = data.get('cart', [])

        payment_request_data = {
            'discountAmount': discount_amount,
            'cartItems': cart_items
        }

        payment_response = requests.get(f'{PAYMENT_MICROSERVICE_URL}/get_payment_url', json=payment_request_data)

        payment_url = payment_response.json()      

        # Create order data to be sent to order microservice (clarise's part)
        order_data = {
                    "email" : email,
                    "order_id": order_id,
                    "item": {
                        "product_name": product_name,
                        "price": price,
                        "quantity": quantity
                    }
                }

        # Send order data to the order microservice
        order_response = requests.post(f'{ORDER_MICROSERVICE_URL}/create_order', json=order_data)
        if order_response.status_code != 200:
            return jsonify({"error": "Failed to create order"}), 500
        
        # Order successfully created
        order_id = order_response.json().get('order_id')

        # Return the order data along with the response
        return jsonify({
            "message": "Order created successfully",
            "order_data": order_data,
        }), 200

    except Exception as e:
        return str(e), 500
    # discount_amount = request.form.get('discount_amount')
    # # Assuming the payment service expects JSON data
    # payment_response = requests.post(f'{PAYMENT_MICROSERVICE_URL}/get_payment_url', json={'discount_amount': discount_amount})

    # # Check if the response is JSON
    # if 'application/json' in payment_response.headers.get('Content-Type'):
    #     try:
    #         payment_url = payment_response.json()
    #         return jsonify(payment_url), 200
    #     except ValueError:  # includes simplejson.decoder.JSONDecodeError
    #         return jsonify({"error": "Failed to decode JSON"}), 500
    # else:
    #     return jsonify({"error": "Expected JSON response"}), 500


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'checkout.session.completed':
      session = event['data']['object']
      print(json.dumps(session, indent=4))
      payment_status = session.get('payment_status')
      print("Payment Status:", payment_status)
      
      # Accessing the customer email from customer_details
      customer_email = session.get('customer_details', {}).get('email')
      print("Customer Email:", customer_email)
      
      # Accessing the total amount
      amount_total = session.get('amount_total')
      print("Total Amount:", amount_total / 100)

      print(tcart, tpoints)
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)



if __name__ == '__main__':
    app.run(debug=True, port=5008)