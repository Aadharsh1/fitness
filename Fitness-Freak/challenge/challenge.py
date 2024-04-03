from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from flasgger import Swagger

app = Flask(__name__)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/challenge'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize flasgger 
app.config['SWAGGER'] = {
    'title': 'Challenge microservice API',
    'version': 1.0,
    "openapi": "3.0.2",
    'description': 'Allows create, retrieve, update, and delete of challenges'
}
swagger = Swagger(app)


class Challenge(db.Model):
    __tablename__ = 'challenge'

    id = db.Column(db.String(5), primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(64), nullable=False)
    reps = db.Column(db.String(64), nullable=False)
    fitnessLevel = db.Column(db.String(64), nullable=False)
    loyaltyPoints = db.Column(db.Integer)

    def __init__(self, id, title, description, reps, fitnessLevel, loyaltyPoints):
        self.id = id
        self.title = title
        self.description = description
        self.reps = reps
        self.fitnessLevel = fitnessLevel
        self.loyaltyPoints = loyaltyPoints

    def json(self):
        return {"id": self.id, "title": self.title, "description": self.description, "reps": self.reps, "fitnessLevel": self.fitnessLevel, "loyaltyPoints": self.loyaltyPoints}

@app.route("/challenge")
def get_all():
    """
    Get all challenges
    ---
    responses:
        200:
            description: Return all challenges
        404:
            description: No challenges

    """

    challengelist = db.session.scalars(db.select(Challenge)).all()

    if len(challengelist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "challenges": [challenge.json() for challenge in challengelist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no challenges."
        }
    ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


