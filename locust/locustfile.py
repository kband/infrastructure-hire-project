# https://github.com/locustio/locust/blob/master/examples/basic.py
from locust import HttpLocust, TaskSet, task, between, constant_pacing

def index(l):
    l.client.get("/")

def status(l):
    l.client.get("/status")

def slow(l):
    l.client.get("/slow/25")

class UserTasks(TaskSet):
    # one can specify tasks like this
    tasks = [index, status, slow]

class WebsiteUser(HttpLocust):
    """
    Locust user class that does requests to the locust web server running on localhost
    """
    wait_time = constant_pacing(1)
    task_set = UserTasks