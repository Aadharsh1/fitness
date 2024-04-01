from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/error', methods=['GET'])
def error_handler():
    error_info = request.get_json()
    return error_info, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5011)
