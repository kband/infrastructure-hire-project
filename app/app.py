# app.py - a minimal flask api using flask_restful
from flask import Flask, abort, Response, send_file
from flask_restful import Resource, Api
from os import environ
import boto3
import botocore

app = Flask(__name__)
api = Api(app)

APP_VERSION = "20.01.001"
# if running locally default to 'dev' environment
BUCKET_NAME = environ.get('BUCKET_NAME', 'ops-hire-project-nic-dev')

def fib(n):
    if n < 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

# A 'slow' route that takes a parameter and calculates the Fibonacci number
# Simulates waiting on a request to another microservice
@app.route("/slow/", defaults={'param': 1})
@app.route("/slow/<int:param>")
def VariableSlowHelloWorld(param):
    f = fib(param)
    return {'slowello': f'world: {f}'}

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

# downloads a files from s3 (will work with sub folders as well) and pipes it back as an attachment/download.
@app.route("/fetch/<path:file_name>")
def fetch(file_name):
    client = boto3.client('s3')

    try:
        file = client.get_object(Key=file_name, Bucket=BUCKET_NAME)
    except botocore.exceptions.ClientError as e:
        # since we don't have have 's3:ListBucket' the expected 404 is actually a 403
        if e.response['ResponseMetadata']['HTTPStatusCode'] == 403:
            abort(404, "The object does not exist.")
        else:
            raise

    return send_file(file['Body'], as_attachment=True, mimetype="application/octet-stream", attachment_filename=file_name)


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')