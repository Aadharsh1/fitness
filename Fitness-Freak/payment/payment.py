from flask import Flask, jsonify, request, render_template
import stripe, os 
import json

from flask_cors import CORS
app = Flask(__name__)
CORS(app)

stripe.api_key = 'sk_test_51OuT5rDip6VoQJfrbgZM63TUyy4WeWzG2JCjJmMXwAMmJ0eSLL3LkZtlUKrUjCrjdQr6dEUD4lac2MQonS304vtL00cbcZkXtH'

YOUR_DOMAIN = 'http://127.0.0.1:5007'

@app.route('/get_payment_url', methods=['GET'])
def get_payment_url():
            data = request.get_json()
            discount_amount = data.get('discount_amount')
            cart = data.get('cart')
            # user_data = data.get('user_data')  # Directly a dictionary
            # cart = user_data.get('cart', [])
            # cart = json.loads(cart)
            # print(type(cart))
            # print(data)
            total = (sum(item['price'] * item['quantity'] for item in cart)) * 100
            # print(total)
            discount_percentage = (float(discount_amount) / total ) 
            # print(discount_percentage)
            # print(discount_percentage)
            checkout_items = []
            for item in cart:
                # print(item)
                discounted_price = float(item['price'] * (1-discount_percentage)) * 100   # Apply discount
                # print(discounted_price)
                checkout_items.append({
                    'price_data': {
                        'currency': 'sgd',
                        'unit_amount': int(discounted_price),  # Adjusted for discount
                        'product_data': {
                            'name': f"{item['title']} (Discount Applied)",
                        },
                    },
                    'quantity': item['quantity'],
                })
            
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=checkout_items,

                mode='payment',
                success_url= 'http://127.0.0.1:5008' + '/success',
                cancel_url= 'http://127.0.0.1:5008' + '/cancel',
            )
            return checkout_session.url, 200

if __name__ == '__main__':
    app.run(debug=True, port = 5007)

