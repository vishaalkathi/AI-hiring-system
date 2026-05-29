import requests #to make http calls from python
from backend.app.core.config import GITHUB_TOKEN

BASE_URL = "https://api.github.com"

headers = {
    "Accept" : "application/vnd.github+json",    #get data in json format
    "Authorization" : f"Bearer {GITHUB_TOKEN}"
}

def get_user(username: str):
    url = f"{BASE_URL}/users/{username}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Return the user data
    else:
        raise Exception(f"User {username} not found. Status code: {response.status_code}")
    
def get_repos(username: str):
    url = f"{BASE_URL}/users/{username}/repos"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Return the list of repositories
    else:
        raise Exception(f"Could not fetch repositories for user {username}. Status code: {response.status_code}")
    
