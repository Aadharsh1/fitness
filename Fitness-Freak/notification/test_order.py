from notification import send_order, get_user_data, connection
import pika
import json

# Invoke send_purchase_email function
user_id = "h5gSBrTxNX2Tc0Lx4N1V"
user_email, user_name, lpoints, user_cart = get_user_data(user_id)

if user_email is not None and user_cart is not None and user_name is not None:
    send_order(user_email, user_name, user_cart)
else:
    print("Failed to retrieve user data.")

channel = connection.channel()

# # Define the message payload
message = {
    'user_id': user_id
}

# Publish the message to the 'notifications' queue
channel.basic_publish(exchange='', routing_key='notifications', body=json.dumps(message))

print("Message sent to notifications queue")
connection.close()
