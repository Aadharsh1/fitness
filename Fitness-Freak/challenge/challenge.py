from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from flasgger import Swagger

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/challenge'
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
   
@app.route("/challenge/<string:id>")
def find_by_id(id):
    """
    Get a book by its ID
    ---
    parameters:
        -   in: path
            name: id
            required: true
    responses:
        200:
            description: Return the challenge with the specified ID
        404:
            description: No challenge with the specified ID found

    """

    challenge = db.session.scalars(
        db.select(Challenge).filter_by(id=id).
        limit(1)
).first()

    if challenge:
        return jsonify(
            {
                "code": 200,
                "data": challenge.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Challenge not found."
        }
    ), 404

@app.route("/challenge/<string:id>", methods=['POST'])
def create_challenge(id):
    """
    Create a challenge by its ID
    ---
    parameters:
        -   in: path
            name: id
            required: true
    requestBody:
        description: Challenge's details
        required: true
        content:
            application/json:
                schema:
                    properties:
                        title: 
                            type: string
                            description: Challenge's title
                        description:
                            type:string
                            description: Challenge's description
                        reps: 
                            type: integer
                            description: Challenge's rep count
                        fitnessLevel: 
                            type: string
                            description: User's fitness level
                        loyaltyPoints:
                            type:integer
                            description: How many loyalty points user will receive upon completion

    responses:
        201:
            description: Challenge created
        400:
            description: Challenge already exists
        500:
            description: Internal server error

    """

    if (db.session.scalars(
        db.select(Challenge).filter_by(id=id).
        limit(1)
).first()
):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "id": id
                },
                "message": "Challenge already exists."
            }
        ), 400

    data = request.get_json()
    challenge = Challenge(id, **data)

    try:
        db.session.add(challenge)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "id": id
                },
                "message": "An error occurred creating the challenge."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": challenge.json()
        }
    ), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


