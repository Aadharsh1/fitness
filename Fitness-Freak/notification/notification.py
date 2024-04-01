#pip install -r requirements.txt
# pip install mailjet_rest

import json, pika, sys, time
from mailjet_rest import Client

hostname = "localhost" 
port = 5672      
exchangename = "notification" # exchange name
exchangetype = "topic" # - use a 'topic' exchange to enable interaction  

# function to create a connection to the broker
def create_connection(max_retries=12, retry_interval=5):
    print('amqp_connection: Create_connection')
    retries = 0
    connection = None
    
    # loop to retry connection upto 12 times with a retry interval of 5 seconds
    while retries < max_retries:
        try:
            print('amqp_connection: Trying connection')
            # connect to the broker
            connection = pika.BlockingConnection(pika.ConnectionParameters
                                (host=hostname, port=port,
                                 heartbeat=3600, blocked_connection_timeout=3600)) 
            print("amqp_connection: Connection established successfully")
            break 
        except pika.exceptions.AMQPConnectionError as e:
            print(f"amqp_connection: Failed to connect: {e}")
            retries += 1
            print(f"amqp_connection: Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    
    if connection is None:
        raise Exception("Unable to establish a connection to RabbitMQ after multiple attempts")
    return connection

# function to check if the exchange exists
def check_exchange(channel, exchangename, exchangetype):
    try:    
        channel.exchange_declare(exchangename, exchangetype, durable=True, passive=True)         
    except Exception as e:
        print('Exception:', e)
        return False
    return True

#to create a connection to the broker
def create_connection(max_retries=12, retry_interval=5):
    print('amqp_setup:create_connection')
    
    retries = 0
    connection = None
    
    # loop to retry connection upto 12 times with a retry interval of 5 seconds
    while retries < max_retries:
        try:
            print('amqp_setup: Trying connection')
            # connect to the broker and set up a communication channel in the connection
            connection = pika.BlockingConnection(pika.ConnectionParameters
                                (host=hostname, port=port,
                                 heartbeat=3600, blocked_connection_timeout=3600)) 
            print("amqp_setup: Connection established successfully")
            break  # Connection successful, exit the loop
        except pika.exceptions.AMQPConnectionError as e:
            print(f"amqp_setup: Failed to connect: {e}")
            retries += 1
            print(f"amqp_setup: Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)

    if connection is None:
        raise Exception("amqp_setup: Unable to establish a connection to RabbitMQ after multiple attempts.")

    return connection

def create_channel(connection):
    print('amqp_setup:create_channel')
    channel = connection.channel()
    # Set up the exchange if the exchange doesn't exist
    print('amqp_setup:create exchange')
    channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True) # 'durable' makes the exchange survive broker restarts
    return channel

#function to create queues
def create_queues(channel):
    print('amqp_setup:create queues')
    create_error_queue(channel)
    create_activity_log_queue(channel)

# function to create Activity_Log queue  
def create_activity_log_queue(channel):
    print('amqp_setup:create_activity_log_queue')
    a_queue_name = 'Activity_Log'
    channel.queue_declare(queue=a_queue_name, durable=True) # 'durable' makes the queue survive broker restarts
    channel.queue_bind(exchange=exchangename, queue=a_queue_name, routing_key='#')
    
# function to create Error queue
def create_error_queue(channel):
    print('amqp_setup:create_error_queue')
    e_queue_name = 'Error'
    channel.queue_declare(queue=e_queue_name, durable=True) 
    channel.queue_bind(exchange=exchangename, queue=e_queue_name, routing_key='*.error')

# Connect to RabbitMQ
connection = create_connection()
channel = connection.channel()
channel.queue_declare(queue='send_lpoints')
channel.queue_declare(queue='send_order')

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
        "Your current loyalty points balance is: "  + str(user_points) + "<br/>"
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
def send_order(user_email, user_name, user_cart):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
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
            "Name": user_name,
            "Cart": user_cart["items"]
            
            }
        ],
        "Subject": "Fitness Freak Successful Order Creation",
        "HTMLPart": "Dear " + user_name + ",<br /><br/>"
        "Thank you for shopping with us! Your order has been received and is being processed. Your order details are below for your reference. <br/><br/>"
        "You bought: <br/>" + cart_html + "<br/>"
        "Hope you have a great day, thank you! <br/><br/>"
        "Cheers, <br/>"
        "Fitness Freaks", 
        }
        ]
    }
    # Send the email
    try:
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())
        # Publish a message to the 'notifications' queue
        message = {
            'user_name': user_name
        }
        channel.basic_publish(exchange='', routing_key='notifications', body=json.dumps(message))
        print("Message sent to notifications queue")
    except Exception as e:
        # print("Error sending message:", e)
        print({"code": 404, "message": "Error, fail to send email."})

# Callback function for consuming messages from RabbitMQ
def callback(ch, method, properties, body, user_email, user_name, user_cart, user_points):
    data = json.loads(body)
    user_id = data.get('user_id')
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
        connection = create_connection()
        channel = create_channel(connection)
        create_queues(channel)
        receiveNotifications()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)




