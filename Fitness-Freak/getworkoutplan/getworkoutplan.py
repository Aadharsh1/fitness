import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
USER_MICROSERVICE_URL = 'http://127.0.0.1:5003'
FITNESS_ASSESSMENT_URL = 'http://127.0.0.1:5001'
WORKOUT_PLANNER_URL = 'http://127.0.0.1:5005'

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
    app.run(debug=True, port=5002)

    
# @app.route('/get_workout_plan', methods=['GET'])
# def get_workout_plan():
#     user_id = request.args.get('user_id')
#     user_response = requests.get(f'{USER_MICROSERVICE_URL}/users/{user_id}')
#     if user_response.status_code != 200:
#         return jsonify({"error": "User not found"}), 404
    
#     user_data = user_response.json()
#     print("User data from User Microservice:", user_data)
#     fitness_status_response = requests.get(f'{FITNESS_ASSESSMENT_URL}/calculate_bmi', params=user_data)
#     if fitness_status_response.status_code != 200:
#         return jsonify({"error": "Could not calculate BMI"}), fitness_status_response.status_code
    
#     fitness_status_data = fitness_status_response.json()

#     workout_plan_response = requests.get(f'{WORKOUT_PLANNER_URL}/workoutplanner/{user_id}', params=fitness_status_data)
#     if workout_plan_response.status_code != 200:
#         return jsonify({"error": "Workout plan not found"}), 404
    
#     workout_plan_data = workout_plan_response.json()
#     return jsonify(workout_plan_data