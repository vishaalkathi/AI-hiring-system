from backend.app.services.github_analyzer.github_api import get_user, get_repos

username = "pokobholu"

print(get_user(username))
print(get_repos(username))