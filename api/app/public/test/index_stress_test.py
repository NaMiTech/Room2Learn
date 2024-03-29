from locust import HttpUser, TaskSet, task, between


def index(locust):
    locust.client.get("/")


class UserTasks(TaskSet):
    # one can specify tasks like this
    tasks = [index, ]

    # but it might be convenient to use the @task decorator
    @task
    def page404(self):
        self.client.get("/does_not_exist")


class WebsiteUser(HttpUser):
    """
    User class that does requests to the locust web server running on localhost
    """

    host = "http://127.0.0.1:8089"
    wait_time = between(2, 5)
    tasks = [UserTasks]
