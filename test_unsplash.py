
import os
import requests
from admin.config import Config

# Force load the keys we just set in Config to be absolutely sure
# We can also hardcode them here for the test to rule out import issues
ACCESS_KEY = '0uRLpYAEQbLf1qw5DIN1IYy0oRdBX3Uh8ayzoO7Hyfg'
SECRET_KEY = '3whfR8dCArWtdGDYZKA5IsOEFTnFSMqaj3JE4zY_6hU'

print("--- Testing Unsplash API ---")
print(f"Access Key: {ACCESS_KEY}")

url = "https://api.unsplash.com/search/photos"
headers = {
    "Authorization": f"Client-ID {ACCESS_KEY}",
    "Accept-Version": "v1"
}
params = {
    "query": "green",
    "per_page": 1
}

try:
    print(f"Requesting {url}...")
    response = requests.get(url, headers=headers, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Response Text: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total Results: {data['total']}")
    else:
        print("!!! REQUEST FAILED !!!")
except Exception as e:
    print(f"Exception: {e}")
