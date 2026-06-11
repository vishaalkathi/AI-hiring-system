from urllib import response

import requests

from backend.app.services.leetcode_analyzer.leetcode_queries import LEETCODE_QUERIES

url = "https://leetcode.com/graphql"

headers = {
    "Accept" : "application/json",
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://leetcode.com"
}


def execute_query(query: str, variables: dict):
    try:
        response = requests.post(
            url,
            json = {
                "query": query,
                "variables": variables
            },
            headers = headers,
            timeout = 10
        )
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error occurred: {str(e)}"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    

def fetch_leetcode_data(username: str) -> dict:
     data = {}
     for key, q in LEETCODE_QUERIES.items():
        response = execute_query(q["query"], q["variables"](username))
        if "error" in response:
            data[key] = response
        else:
            data[key] = response.get("data", {})  # Safely get 'data' or return empty dict if not present
     
     return data

print(fetch_leetcode_data("pokobholu"))