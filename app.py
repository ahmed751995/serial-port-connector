from flask import Flask, jsonify

# set Flask APP

def create_app(SerialPort):
    app = Flask(__name__)
    
    @app.route('/measure')
    def index():
        value = SerialPort.measure_scaler()
        response  = jsonify({'value': value})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    return app
