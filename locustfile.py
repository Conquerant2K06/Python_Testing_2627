from locust import HttpUser, task, between #type: ignore


class GudlftUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def index(self):
        self.client.get("/")

    @task(2)
    def login(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task(1)
    def points_board(self):
        self.client.get("/points")