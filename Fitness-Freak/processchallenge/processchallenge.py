from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from invokes import invoke_http
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.join(current_dir, '../notification')
sys.path.append(module_dir)

from notification import send_lpoints, connection
import pika, json

app = Flask(__name__)
CORS(app)

verification_url = "http://localhost:5006/get_pict"
error_url = "http://localhost:5011/error"
user_url = 'http://127.0.0.1:5003/update_user_lpoints/'

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

            #notifications?
            user_email, user_name, lpoints= get_user_data(uid)
            if user_email is not None and lpoints is not None and user_name is not None:
                send_lpoints(user_email, user_name, lpoints)
            else:
                print("Failed to retrieve user data.")

            channel = connection.channel()
            message = {
                'user_id': uid
            }
            channel.basic_publish(exchange='', routing_key='lpoints', body=json.dumps(message))
            print("Message sent to notifications queue")
            connection.close()
            #notification end

            return jsonify(response_data), 200

        else:
            return jsonify({"error": "Failed to update loyalty points"}), update_response.status_code
    else:
        # print("Verification Failed, please resubmit photo.") # make this an alert in the UI, v-if... alert...
        # invoke_http(error_url, method = "")
        # return jsonify(response.json()), 400
        error_response = requests.get(error_url, json=response.json())
        return jsonify({'error': 'Verification failed', 'details': error_response.json()}), 400
    
def get_user_data(user_id):
    user_url = 'http://127.0.0.1:5003/get_user_data/' + user_id
    response = requests.get(user_url)
    if response.status_code == 200:
        user_data = response.json()
        user_email = user_data.get('email')
        user_name = user_data.get('name')
        lpoints = user_data.get('loyalty_points')
        return user_email, user_name, lpoints
    else:
        return None, None, None

if __name__ == '__main__':
    app.run(debug=True, port=5012)
