#pip install -r requirements.txt
# pip install mailjet_rest
# npm install firebase-admin

import json, pika, firebase_admin, sys
from firebase_admin import credentials, firestore, messaging
from amqp_connection import create_connection
from amqp_setup import create_channel, create_queues
from mailjet_rest import Client


# Initialize Firebase Admin SDK
cred = credentials.Certificate('fitness-freak-94e2d-firebase-adminsdk-9xqts-c2691de9d2.json')
firebase_admin.initialize_app(cred)

#obtain messaging instance
#use this to send notifications to client apps
messaging = firebase_admin.messaging

# Connect to RabbitMQ
connection = create_connection()
channel = connection.channel()
channel.queue_declare(queue='send_lpoints')
channel.queue_declare(queue='send_order')

# Create a Firestore client
db = firestore.client()

#constants - mailjet
api_key = '5cc6a1bb560de17e3436c05775842281'
api_secret = '0009db80a2e7b995ca791048f36b3b63'


# Function to send email notification for lpoints
def send_lpoints(user_email, user_name, user_points):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
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
            "Name": user_name,
            "Points": user_points
            }
        ],
        "Subject": "Fitness Freak Loyalty Points Balance",
        # "TextPart": "Fitness Freaks email",
        "HTMLPart": "Dear " + user_name + ",<br /><br/>"
        "Thank you for shopping with us! <br/>"
        "Your current loyalty points balance is: "  +str(user_points) + "<br/>"
        "Hope you have a great day, thank you! <br/><br/>"
        "Cheers, <br/>"
        "Fitness Freaks", 
        # "CustomID": "AppGettingStartedTest"
        }
        ]
    }
    # Send the email
    try:
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())
    except Exception as e:
        print("Error sending message:", e)
        print(e.status_code)
        print(e.message)


#Function to send email notification for successful order creation
def send_order(user_email, user_name, user_order):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    cart_html = "<ul>"
    for item in user_order:
        cart_html += "<li>{}</li>".format(item["item"] +  " x" + str(item["quantity"]))
    cart_html += "</ul>"
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
            "Name": user_name,
            "Cart": user_order
            
            }
        ],
        "Subject": "Fitness Freak Successful Order Creation",
        # "TextPart": "Fitness Freaks email",
        "HTMLPart": "Dear " + user_name + ",<br /><br/>"
        "Thank you for shopping with us! Your order has been received and is being processed. Your order details are below for your reference. <br/>"
        "You bought: <br/>" + cart_html + "<br/>"
        "Hope you have a great day, thank you! <br/><br/>"
        "Cheers, <br/>"
        "Fitness Freaks", 
        # "CustomID": "AppGettingStartedTest"
        }
        ]
    }
    # Send the email
    try:
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())
    except Exception as e:
        # print("Error sending message:", e)
        print({"code": 404, "message": "Error, fail to send email."})

# Callback function for consuming messages from RabbitMQ
def callback(ch, method, properties, body):
    data = json.loads(body)
    user_id = data.get('user_id')
    user_email, user_name, user_points, user_cart = get_user_data(user_id)
    notification_queue_key = method.routing_key

    if user_email is not None and user_points is not None and user_name is not None and user_cart is not None:
        print(f"User Email: {user_email}, User Name: {user_name}, Loyalty Points: {user_points}, Cart: {user_cart}")
        if method.routing_key == 'send_order':
            send_order(user_email, user_name, user_cart)
        elif method.routing.key == 'send_lpoints':
            send_lpoints(user_email, user_name, user_points)
        else:
            print("Unknown routing key")
    else:
        # print("Failed to retrieve user data.")
        print({"code": 404, "message": "Error, fail to send email."})

    ch.basic_ack(delivery_tag=method.delivery_tag)

# Function to retrieve user data from Firestore
def get_user_data(user_id):
    # Get user document from Firestore
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()

    # Check if user document exists
    if user_doc.exists:
        # Get email and lpoints values from the user document
        user_data = user_doc.to_dict()
        user_email = user_data.get('email')
        user_points = user_data.get('lpoints')
        user_name = user_data.get('name')
        user_cart = user_data.get('cart')

         # Print out the user data
        print(f"User ID: {user_id}")
        print(f"Email: {user_email}")
        print(f"Name: {user_name}")
        print(f"Loyalty Points: {user_points}")
        print(f"Cart: {user_cart}")

        return user_email, user_name, user_points, user_cart
    else:
        print(f"User with ID {user_id} not found.")
        return None, None, None

# notification_queue_key = method.routing_key

def receiveNotifications():
    try:
        connection = create_connection()
        channel = create_channel(connection)
        create_queues(channel)

        # Set up a consumer and start to wait for incoming messages
        channel.basic_consume(queue='send_order', on_message_callback=callback, auto_ack=False)
        channel.basic_consume(queue='send_lpoints', on_message_callback=callback, auto_ack=False)
        print('notifications: Consuming from queue:', )
        channel.start_consuming()  # an implicit loop waiting to receive messages;
                                   # it doesn't exit by default. Use Ctrl+C to terminate it.
    except pika.exceptions.AMQPError as e:
        print(f"notifications: Failed to connect: {e}")

    except KeyboardInterrupt:
        print("notifications: Program interrupted by user.")

if __name__ == "__main__":
    try:
        receiveNotifications()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


