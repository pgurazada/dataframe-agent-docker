import requests

localurl = "http://localhost:8000/v1/input"

example_input = "How many customers do we have?"

response = requests.post(
    localurl,
    data=example_input
)

response.status_code

response.json()