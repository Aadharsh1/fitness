from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import json, pika

app = Flask(__name__)
CORS(app)

verification_url = "http://verification:5006/get_pict"
error_url = "http://error:5011/error"
user_url = 'http://user:5003/update_user_lpoints/'

@app.route('/processChallenge', methods=['POST'])
def process_challenge():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    print(request.form)
    file = request.files['image']
    title = request.form['challengeTitle']
    loyaltypoints = request.form['loyaltyPoints']
    uid = request.form['uid']
    headers = {'Challenge-Title': title}
    files = {'image': (file.filename, file.stream, file.mimetype)}
    response = requests.get(verification_url, files=files, headers=headers)
    if response.status_code == 200:
        update_url = user_url + uid
        payload = {'lpoints': loyaltypoints}
        print(update_url, loyaltypoints)
        update_response = requests.put(update_url, json=payload)
        if update_response.status_code == 200:
            updated_points_data = update_response.json()  
            newlpoints = updated_points_data.get('newlpoints', 0) 
            response_data = response.json()  
            response_data['updated_lpoints'] = newlpoints

            #notification
            user_email, user_name, lpoints= get_user_data(uid)

            # Create a connection to RabbitMQ
            connection = create_connection()
            channel = connection.channel()

            # Define the exchange and routing key
            exchange_name = 'notification'
            routing_key = 'send_lpoints'

            # Define the message to be published
            data = create_email_lpoints(user_email, user_name, lpoints)

            # Publish the message
            try:
                channel.basic_publish(exchange='notification', routing_key='send_lpoints', body=json.dumps(data))
                print("Message sent to send_order queue")
            except Exception as e:
                print({"code": 404, "message": "Error, fail to send email."})
                publish_message(channel, exchange_name, routing_key, data)
                # Close the connection
                connection.close()
            #notification end
            return jsonify(response_data), 200

        else:
            return jsonify({"error": "Failed to update loyalty points"}), update_response.status_code
    else:
        error_response = requests.get(error_url, json=response.json())
        return jsonify({'error': 'Verification failed', 'details': error_response.json()}), 400
    
def get_user_data(user_id):
    user_url = 'http://user:5003/users/' + user_id
    response = requests.get(user_url)  
    if response.status_code == 200:
        user_data = response.json()
        user_email = user_data.get('email')
        lpoints = user_data.get('lpoints')
        return user_email, "Customer", lpoints
    else:
        return None, "Customer", 0
    


#notification part
# Function to create a connection to RabbitMQ
def create_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',heartbeat=3600, blocked_connection_timeout=3600))
    return connection

# Function to publish a message to RabbitMQ
def publish_message(channel, exchange_name, routing_key, message):
    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)
    print(" [x] Sent message:", message)

def create_email_lpoints(user_email, user_name, user_points):
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
        "HTMLPart": "Dear " + str(user_name) + ",<br /><br/>"
        "Great job on completing the challenge! <br/>"
        "Your current loyalty points balance is: "  + str(user_points) + "<br/>"
        "Hope you have a great day, thank you! <br/><br/>"
        "Cheers, <br/>"
        "Fitness Freaks", 
        }
        ]
    }
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5012)