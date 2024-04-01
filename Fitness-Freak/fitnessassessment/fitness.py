from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/calculate_bmi', methods=['GET']) 
def calculate_bmi():
    user_data = request.json  
    height = user_data.get('height', None)  
    weight = user_data.get('weight', None)       
    if height is not None and weight is not None:
        height_meters = height / 100 
        bmi = weight / (height_meters * height_meters)
        if bmi <= 18.5:
            fitness_status = 'Underweight'
        elif 18.5 < bmi <= 24.9:
            fitness_status = 'Healthy'
        elif 24.9 < bmi <=29.9:
            fitness_status = 'Overweight'
        else:
            fitness_status = 'Obese'
        return jsonify({"fitness_status": fitness_status}), 200
    else:
        return jsonify({"error": "Height or weight data not found for the user"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port = 5001)