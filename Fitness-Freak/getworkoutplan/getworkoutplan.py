import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
USER_MICROSERVICE_URL = 'http://user:5003'
FITNESS_ASSESSMENT_URL = 'http://fitness:5001'
WORKOUT_PLANNER_URL = 'http://workoutplanner:5005'

@app.route('/get_workout_plan/<user_id>', methods=['GET'])
def get_fitness_status(user_id):
    user_response = requests.get(f'{USER_MICROSERVICE_URL}/users/{user_id}')
    if user_response.status_code != 200:
        return jsonify({"error": "User not found"}), 404
    
    user_data = user_response.json()

    fitness_status_response = requests.get(f'{FITNESS_ASSESSMENT_URL}/calculate_bmi', json=user_data)
    if fitness_status_response.status_code != 200:
        return jsonify({"error": "Could not calculate BMI"}), fitness_status_response.status_code
    
    fitness_status_data = fitness_status_response.json()
    workout_plan_response = requests.get(f'{WORKOUT_PLANNER_URL}/workoutplanner', json=fitness_status_data)
    if workout_plan_response.status_code != 200:
        return jsonify({"error": "Workout plan not found"}), 404
    return workout_plan_response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5002)

    
