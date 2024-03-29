import os
from flask import Flask, redirect, request

import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51OuT5rDip6VoQJfrbgZM63TUyy4WeWzG2JCjJmMXwAMmJ0eSLL3LkZtlUKrUjCrjdQr6dEUD4lac2MQonS304vtL00cbcZkXtH'

app = Flask(__name__)

YOUR_DOMAIN = 'http://127.0.0.1:4242'

@app.route('/create_checkout_session', methods=['POST'])
def create_checkout_session():
    try:
        
        checkout_session = stripe.checkout.Session.create(
            
            line_items = [ {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': '{{price_1OvIwEDip6VoQJfrRk2kFd6R}}',
                    'quantity': 1,
                },],
            payment_method_types=['card'],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
    
        )

    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    app.run(port=4242)