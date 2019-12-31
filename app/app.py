# app.py - a minimal flask api using flask_restful
from flask import Flask, abort, Response
from flask_restful import Resource, Api
from time import sleep
from os import environ

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@app.route("/slow")
def SlowHelloWorld():
    sleep(1)
    return {'slowello': 'world: 1'}

@app.route("/slow/<int:param>")
def VariableSlowHelloWorld(param):
    sleep(param)
    return {'slowello': f'world: {param}'}

@app.route("/oh_no")
def fail():
    #abort(503)
    abort(503, description="Well this is embarrasing...")

@app.route("/status")
def status():
    return {'status': 'OK',
            'hostname': environ['HOSTNAME'],
            'python': environ['PYTHON_VERSION'],
            'region': environ['AWS_REGION']
            }

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')