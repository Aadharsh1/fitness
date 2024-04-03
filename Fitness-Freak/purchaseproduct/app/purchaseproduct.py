import requests
from flask import Flask, jsonify, render_template, request
import stripe
from flask_cors import CORS
import json, pika

stripe.api_key = 'sk_test_51OuT5rDip6VoQJfrbgZM63TUyy4WeWzG2JCjJmMXwAMmJ0eSLL3LkZtlUKrUjCrjdQr6dEUD4lac2MQonS304vtL00cbcZkXtH'
endpoint_secret = 'whsec_6c9ba7e888b57c5367963e9546d5c1df0a9d59c8ecdacf687b010f0938d52e03'


app = Flask(__name__, template_folder='templates')
CORS(app)
USER_MICROSERVICE_URL = 'http://user:5003'
PAYMENT_MICROSERVICE_URL = 'http://payment:5007'
ORDER_MICROSERVICE_URL = 'http://order:5010'
PRODUCT_MICROSERVICE_URL = 'http://product:5004'

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

@app.route('/get_user_points/<uid>', methods=['GET'])
def get_user_points(uid):
    user_response = requests.get(f'{USER_MICROSERVICE_URL}/user_lpoints/{uid}')
    if user_response.status_code == 200:
        return jsonify(user_response.json()), 200
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/create_checkout_session', methods=['POST'])
def create_checkout_session():
    try:
        discount_amount = request.form['discountAmount']
        cart = request.form['cart']
        uid = request.form['userId']
        
        payment_response = requests.get(f'{PAYMENT_MICROSERVICE_URL}/get_payment_url',json={
        'discount_amount': discount_amount,
        'cart': json.loads(cart),
        'uid': uid  
    })
        
        if payment_response.status_code == 200:
            # Extract the payment URL from the response and send it back
            payment_url = payment_response.text
            return payment_url, 200
        else:
            return jsonify({"error": "Failed to get payment URL"}), payment_response.status_code
            
    except Exception as e:
        return str(e), 500
    


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
        payment_status = session.get('payment_status')
        
        # Accessing the customer email from customer_details
        customer_email = session.get('customer_details', {}).get('email')
        
        # Accessing the total amount
        amount_total = session.get('amount_total')
        metadata = session.get('metadata', {})
        cart_json = metadata.get('cart', '{}')
        cart = json.loads(cart_json) # changes the cart to object
        payloadproduct = {
                'cart': cart
            }
        databaseupdate_url = PRODUCT_MICROSERVICE_URL + '/product/modify'
        databaseupdate_response = requests.put(databaseupdate_url, json = payloadproduct)
        discount_amount = metadata.get('discount_amount', '')
        uid = metadata.get('uid', '')
        update_url = USER_MICROSERVICE_URL+ '/update_user_lpoints/' + uid
        payload1 =  {'lpoints': -int(discount_amount)}
        user_points_update_response = requests.put(update_url, json=payload1)
        if user_points_update_response.status_code == 200:
            print('user points updated successfully')
        payload = {
                'cart': cart,
                'discount_amount': discount_amount,
                'email': customer_email
            }
        request_url = ORDER_MICROSERVICE_URL + '/create_order'
        # Make the POST request with payload
        update_response = requests.post(request_url, json=payload)
        # Check the response
        user = update_response.json()
        if update_response.status_code == 200:
            print("Order created successfully.")  

            # Create a connection to RabbitMQ
            connection = create_connection()
            channel = connection.channel()

            # Define the exchange and routing key
            exchange_name = 'notification'
            routing_key = 'send_order'

            # Define the message to be published
            data = create_email_order(user["email"], user)

            # Publish the message
            try:
                channel.basic_publish(exchange='notification', routing_key='send_order', body=json.dumps(data))
                print("Message sent to send_order queue")
            except Exception as e:
                print("Error, fail to send email.")
                publish_message(channel, exchange_name, routing_key, data)
                # Close the connection
                connection.close()

             
        else:
            print("Failed to create order. Status code:", update_response.status_code)

    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)



# Function to create a connection to RabbitMQ
def create_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',heartbeat=3600, blocked_connection_timeout=3600))
    return connection

# Function to publish a message to RabbitMQ
def publish_message(channel, exchange_name, routing_key, message):
    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)
    print(" [x] Sent message:", message)


#Function to send email notification for successful order creation
def create_email_order(user_email, user_cart):
    no = 1
    cart_html = "<table border='1'><tr><td>No.</td><td>Product</td><td>Quantity</td><td>Price</td></tr>"
    for i in range(len(user_cart["items"])):
        item = user_cart["items"][i]
        cart_html += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(str(no), str(item["title"]), str(item["quantity"]), str(item["price"]))
        no += 1
    cart_html += "<tr><td colspan='3'>Loyalty Points used:</td><td>{}</td></tr>".format(str(user_cart["lpoints_used"]))
    cart_html += "<tr><td colspan='3'>Total price before discount:</td><td>{}</td></tr>".format(str(user_cart["price_before_discount"]))
    cart_html += "<tr><td colspan='3'>Total price after discount:</td><td>{}</td></tr>".format(str(user_cart["final_total_price"]))
    cart_html += "</table>"
    data = {
    'Messages': [
        {
        "From": {
            "Email": "fitnessfreakscompany888@gmail.com",
            "Name": "Fitness"
        },
        "To": [
            {
            "Email": user_email,
            "Cart": user_cart["items"]
            
            }
        ],
        "Subject": "Fitness Freak Successful Order Creation",
        "HTMLPart": "Dear Customer,<br /><br/>"
        "Thank you for shopping with us! Your order has been received and is being processed. Your order details are below for your reference. <br/><br/>"
        "You bought: <br/>" + cart_html + "<br/>"
        "Hope you have a great day, thank you! <br/><br/>"
        "Cheers, <br/>"
        "Fitness Freaks", 
        }
        ]
    }
    return data
#notification end


if (__name__ == '__main__'):
    app.run(host='0.0.0.0', debug=True, port=5008)