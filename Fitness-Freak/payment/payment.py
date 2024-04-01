from flask import Flask, jsonify, request, render_template
import stripe, os 
import json

from flask_cors import CORS
app = Flask(__name__)
CORS(app)

stripe.api_key = 'sk_test_51OuT5rDip6VoQJfrbgZM63TUyy4WeWzG2JCjJmMXwAMmJ0eSLL3LkZtlUKrUjCrjdQr6dEUD4lac2MQonS304vtL00cbcZkXtH'
endpoint_secret = 'whsec_6c9ba7e888b57c5367963e9546d5c1df0a9d59c8ecdacf687b010f0938d52e03'

YOUR_DOMAIN = 'http://127.0.0.1:5007'

@app.route('/get_payment_url', methods=['GET'])
def get_payment_url():
            data = request.get_json()
            discount_amount = data.get('discount_amount')
            cart = data.get('cart')
            total = (sum(item['price'] * item['quantity'] for item in cart)) * 100
            discount_percentage = (float(discount_amount) / total ) 
            checkout_items = []
            for item in cart:
                discounted_price = float(item['price'] * (1-discount_percentage)) * 100   
                checkout_items.append({
                    'price_data': {
                        'currency': 'sgd',
                        'unit_amount': int(discounted_price),  
                        'product_data': {
                            'name': f"{item['title']} (Discount Applied)",
                        },
                    },
                    'quantity': item['quantity'],
                })
            
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=checkout_items,
                metadata={'cart': json.dumps(cart),
                          'discount_amount': str(discount_amount)},
                mode='payment',
                success_url= 'http://127.0.0.1:5008' + '/success',
                cancel_url= 'http://127.0.0.1:5008' + '/cancel',
            )
            return checkout_session.url, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port = 5007)