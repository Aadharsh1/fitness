from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from flasgger import Swagger

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/product'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@host.docker.internal:3306/product'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize flasgger 
app.config['SWAGGER'] = {
    'title': 'Product microservice API',
    'version': 1.0,
    "openapi": "3.0.2",
    'description': 'Allows create, retrieve, update, and delete of products'
}
swagger = Swagger(app)


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.String(5), primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    availability = db.Column(db.Integer)
    image = db.Column(db.String(64), nullable=False)

    def __init__(self, id, title, description, price, availability, image):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.availability = availability
        self.image = image

    def json(self):
        return {"id": self.id, "title": self.title, "description": self.description, "price": self.price, "availability": self.availability, "image": self.image}

@app.route("/product")
def get_all():
    """
    Get all products
    ---
    responses:
        200:
            description: Return all products
        404:
            description: No products

    """

    productlist = db.session.scalars(db.select(Product)).all()

    if len(productlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "products": [product.json() for product in productlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no products."
        }
    ), 404
   
@app.route("/product/<string:id>")
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
            description: Return the product with the specified ID
        404:
            description: No product with the specified ID found

    """

    product = db.session.scalars(
        db.select(Product).filter_by(id=id).
        limit(1)
).first()

    if product:
        return jsonify(
            {
                "code": 200,
                "data": product.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Product not found."
        }
    ), 404

@app.route("/product/<string:id>", methods=['POST'])
def create_product(id):
    """
    Create a product by its ID
    ---
    parameters:
        -   in: path
            name: id
            required: true
    requestBody:
        description: Product's details
        required: true
        content:
            application/json:
                schema:
                    properties:
                        title: 
                            type: string
                            description: Product's title
                        description:
                            type:string
                            description: Product's description
                        price: 
                            type: number
                            description: Product's price
                        availability: 
                            type: integer
                            description: Number in stock
                        image:
                            type:string
                            description: Relative path to image

    responses:
        201:
            description: Product created
        400:
            description: Product already exists
        500:
            description: Internal server error

    """

    if (db.session.scalars(
        db.select(Product).filter_by(id=id).
        limit(1)
).first()
):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "id": id
                },
                "message": "Product already exists."
            }
        ), 400

    data = request.get_json()
    product = Product(id, **data)

    try:
        db.session.add(product)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "id": id
                },
                "message": "An error occurred creating the product."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": product.json()
        }
    ), 201

@app.route("/product/modify/<string:id>/<string:availability>", methods=['PUT'])
def modify_product(id, availability):
    """
    Modify the availability of a product by its ID
    ---
    parameters:
        -   in: path
            name: id
            required: true
        -   in: path
            name: availability
            required: true
        requestBody:
            description: This parameter is ignored, as availability is passed in the URL
    responses:
        200:
            description: Product availability modified successfully
        404:
            description: Product with the specified ID not found
        500:
            description: Internal server error
    """

    product = db.session.query(Product).filter_by(id=id).first()

    if product:
        try:
            new_availability = int(availability)
        except ValueError:
            return jsonify(
                {
                    "code": 400,
                    "message": "Availability must be an integer value."
                }
            ), 400

        product.availability = new_availability

        try:
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": product.json(),
                    "message": "Product availability modified successfully."
                }
            )
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "id": id
                    },
                    "message": f"An error occurred modifying the product availability: {str(e)}"
                }
            ), 500
    else:
        return jsonify(
            {
                "code": 404,
                "message": "Product not found."
            }
        ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)


