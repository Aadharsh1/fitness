from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

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
            return jsonify(response_data), 200

        else:
            return jsonify({"error": "Failed to update loyalty points"}), update_response.status_code
    else:
        # print("Verification Failed, please resubmit photo.") # make this an alert in the UI, v-if... alert...
        # invoke_http(error_url, method = "")
        # return jsonify(response.json()), 400
        error_response = requests.get(error_url, json=response.json())
        return jsonify({'error': 'Verification failed', 'details': error_response.json()}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5012)
