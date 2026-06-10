import requests

url = "https://leetcode.com/graphql"

headers = {
    "Accept" : "application/json"
}

query = """
query languageStats($username: String!) {
    matchedUser(username: $username) {
        languageProblemCount {
            languageName
            problemsSolved
        }
    }
}
"""

variables = {
    "username": "pokobholu"
}

response = requests.post(
    url,
    json = {
        "query": query,
        "variables": variables
    }
)

print(response.status_code)
print(response.json())