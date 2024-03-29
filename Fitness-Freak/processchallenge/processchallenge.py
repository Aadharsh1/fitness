from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

verification_url = "http://localhost:5006/get_pict"
error_url = "http://localhost:5011/error"

@app.route('/processChallenge', methods=['POST'])
def process_challenge():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']
    title = request.form['challengeTitle']
    loyalpoints = request.form['loyaltyPoints']
    headers = {'Challenge-Title': title}
    files = {'image': (file.filename, file.stream, file.mimetype)}
    response = requests.get(verification_url, files=files, headers=headers)
    if response.status_code == 200:
        # print(jsonify(response.json()), 200)
        return jsonify(response.json()), 200
    else:
        # print("Verification Failed, please resubmit photo.") # make this an alert in the UI, v-if... alert...
        # invoke_http(error_url, method = "")
        # return jsonify(response.json()), 400
        error_response = requests.get(error_url, json=response.json())
        return jsonify({'error': 'Verification failed', 'details': error_response.json()}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5012)
