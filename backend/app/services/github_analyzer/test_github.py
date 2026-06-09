from backend.app.services.github_analyzer.github_api import get_user, get_repos
from backend.app.services.github_analyzer.repo_analyzer import extract_features
from backend.app.services.github_analyzer.metrics import github_score 

username_list = ["pokobholu", "handshek", "ThePrimeagen"]

for i in username_list:
    user_data = get_user(i)
    repos = get_repos(i)
    features = extract_features(user_data, repos)
    score = github_score(features)
    print(f"GitHub Score for {i}: {score}")

