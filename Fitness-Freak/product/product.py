from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from os import environ

from flasgger import Swagger

app = Flask(__name__)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/product'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
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
   
@app.route("/product/modify", methods=['PUT'])
def modify_product():
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
    data = request.json
    cart = data.get('cart', None)
    for item in cart:
        id = item.get('id', None)
        availability = int(item.get('availability',None))
        quantity_purchased = int(item.get('quantity',None))
        new_quantity = availability - quantity_purchased
        product = db.session.query(Product).filter_by(id=id).first()

        if product:
            try:
                new_availability = int(new_quantity)
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
            ), 
    print ('Products updated successfully')
    return jsonify(
                    {
                        "code": 200,
                        "message": "Product availability modified successfully."
                    }
                )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)


