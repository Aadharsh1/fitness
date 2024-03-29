from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/workout_plans' 
db = SQLAlchemy(app)


class Workout(db.Model):
    __tablename__ = 'workouts'
    wid = db.Column(db.Integer, primary_key=True)
    fitness = db.Column(db.String(8), nullable=False)
    day_number = db.Column(db.Integer, nullable=False)
    activity = db.Column(db.String(64), nullable=False)
    descrptn = db.Column(db.String(64))
    exercise = db.Column(db.String(64))
    no_of_sets = db.Column(db.String(64))

@app.route('/workoutplanner', methods=['GET'])
def get_workout_plan():
    fitness_status_data = request.json 
    fitness = fitness_status_data['fitness_status']
    workouts = Workout.query.filter_by(fitness=fitness).all()
    
    # Dictionary to store workouts organized by day_number
    workout_dict = defaultdict(list)
    
    # Group workouts by day_number
    for workout in workouts:
        workout_dict[workout.day_number].append({
            'wid': workout.wid,
            'activity': workout.activity,
            'descrptn': workout.descrptn,
            'exercise': workout.exercise,
            'no_of_sets': workout.no_of_sets
        })
    
     # Convert defaultdict to regular dictionary
    workout_data = dict(workout_dict)
    
    # Dictionary to map day numbers to day labels
    day_labels = {
        1: "Day 1",
        2: "Day 2",
        3: "Day 3",
        4: "Day 4",
        5: "Day 5",
        6: "Day 6",
        7: "Day 7"
    }
    
    # Replace day numbers with day labels
    workout_data_labeled = {day_labels[day]: workouts for day, workouts in workout_data.items()}
    
    
    return jsonify(workout_data_labeled)





if __name__ == '__main__':
    app.run(port=5005, debug=True)
