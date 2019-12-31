# app.py - a minimal flask api using flask_restful
from flask import Flask, abort, Response
from flask_restful import Resource, Api
from time import sleep
from os import environ

app = Flask(__name__)
api = Api(app)

APP_VERSION = "20.01.001"

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

# A 'slow' route that takes 1s to return, or if an int is supplied, will return in int many seconds
# Simulates waiting on a request to another microservice
@app.route("/slow", defaults={'param': 1})
@app.route("/slow/<int:param>")
def VariableSlowHelloWorld(param):
    sleep(param)
    return {'slowello': f'world: {param}'}

# route that throws a 503 error, apps have been known to do this unintentionally from time to time
@app.route("/oh_no")
def fail():
    abort(503, description="Well this is embarrassing...")

# status route for ALB health checks, including debugging data from container
@app.route("/status")
def status():
    return {'status': 'OK',
            'hostname': environ['HOSTNAME'],
            'python': environ['PYTHON_VERSION'],
            'region': environ.get('AWS_REGION', 'non-aws'),
            'app_version': APP_VERSION
            }

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')