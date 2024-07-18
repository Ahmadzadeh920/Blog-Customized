from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    
    def on_start(self):
        response = self.client.post("/accounts/api/v1/api/token/", data={"email":"admin@admin.com", "password":"as@123456"})
        #access =  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxODk5NDA5LCJpYXQiOjE3MjEyOTQ2MDksImp0aSI6IjVhYzRiMmExMTUzNDQwODg4NDU2ZDNhZjhjOTk4NjE2IiwidXNlcl9pZCI6MX0.KdBYG5ilAHrJvNdEZkL2F4wAJrUz6tEvvVXzQolTZW4'
        self.client.headers = {
               "authorization": f"Bearer {response.get('access',None)}"
               }


    @task
    def post_list(self):
        
        self.client.get("/blog/api-v1/post/")
       