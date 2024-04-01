#pip install -r requirements.txt
# pip install mailjet_rest

import json, pika, sys, time
from mailjet_rest import Client

#constants - mailjet
api_key = '5cc6a1bb560de17e3436c05775842281'
api_secret = '0009db80a2e7b995ca791048f36b3b63'

def create_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',heartbeat=3600, blocked_connection_timeout=3600))
    return connection

# Callback function for consuming messages from RabbitMQ
def callback(ch, method, properties, body):
    data = json.loads(body)
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
    print(f"Sending order confirmation")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def receiveNotifications():
    try:
        connection = create_connection()
        channel = create_channel(connection)

        # Set up a consumer and start to wait for incoming messages
        channel.basic_consume(queue='send_order', on_message_callback=callback, auto_ack=False)
        channel.basic_consume(queue='send_lpoints', on_message_callback=callback, auto_ack=False)
        print('notifications: Consuming from queue:', )
        channel.start_consuming()  

    except pika.exceptions.AMQPError as e:
        print(f"notifications: Failed to connect: {e}")

    except KeyboardInterrupt:
        print("notifications: Program interrupted by user.")


def create_channel(connection):
    print('amqp_setup:create_channel')
    channel = connection.channel()
    # Set up the exchange if the exchange doesn't exist
    print('amqp_setup:create exchange')
    channel.exchange_declare(exchange="notification", exchange_type="topic", durable=True) # 'durable' makes the exchange survive broker restarts

    # Declare the queues
    channel.queue_declare(queue='send_lpoints')
    channel.queue_declare(queue='send_order')

    # Bind the queues to the exchange
    channel.queue_bind(exchange='notification', queue='send_lpoints', routing_key='send_lpoints')
    channel.queue_bind(exchange='notification', queue='send_order', routing_key='send_order')

    return channel


if __name__ == "__main__":
    try:
        receiveNotifications()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)




