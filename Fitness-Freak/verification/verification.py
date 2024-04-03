from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_pict', methods=['GET'])
def get_pict():
    # Check if a file is part of the request
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']
    
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Prepare the request for the external API
    files = {'image': (file.filename, file.stream, file.content_type)}
    url = "https://objects-detection.p.rapidapi.com/objects-detection"
    headers = {
        "X-RapidAPI-Key": "b51068ae32msh0fb3d0dd81692bcp1e35e5jsn97186025ca70",
        "X-RapidAPI-Host": "objects-detection.p.rapidapi.com"
    }

    # Forward the file stream directly to the external API
    response = requests.post(url, files=files, headers=headers)
    challenge_title = request.headers.get('Challenge-Title').lower()
    
    # Process and return the response from the external API
    if response.status_code == 200:
        words = response.json()['body']['keywords']
        list1 = [i.lower() for i in words]
        str1 = ''.join(list1)
        str2 = str1.replace(" ", "")
        if 'situp' in challenge_title and 'sit' in str2:
            return jsonify({"success" : "Image verified successfully", 'keywords' : list1}), 200
        if challenge_title in str2:
            return jsonify({"success" : "Image verified successfully", 'keywords' : list1}), 200
        else:
            return jsonify({"error": "keyword not in image", 'keywords' : list1}), 400
    else:
        return jsonify({"error": "Image processing failed"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5006)











# url = "https://objects-detection.p.rapidapi.com/objects-detection"

#     payload = { "url": "https://openmediadata.s3.eu-west-3.amazonaws.com/birds.jpeg" }
#     headers = {
#         "X-RapidAPI-Key": "3a6741047amsh2536f00f02048adp12f17ajsn3220a6165926",
#         "X-RapidAPI-Host": "objects-detection.p.rapidapi.com"
#     }