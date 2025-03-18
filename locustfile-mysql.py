from locust import HttpUser, task, between

class MyFlaskAppUser(HttpUser):
    # Wait time between task executions (in seconds)
    wait_time = between(1, 5)  # Users wait between 1 and 5 seconds between requests

#    @task
#    def hello_world_get(self):
#        # GET request to the /helloworld endpoint
#        self.client.get("/helloworld")
#
#    @task
#    def hello_world_post(self):
#        # POST request to the /helloworld endpoint
#        self.client.post("/helloworld", data={"lang": "en"})
#
#    @task
#    def get_requests(self):
#        # GET request to the /requests endpoint
#        self.client.get("/requests")
    @task
    def get_requests(self):
        # GET request to the /requests endpoint
        self.client.get("/")
