def extract_features(user_data, repos):
    total_stars = 0
    languages = set()
    active_repos = 0

    for repo in repos:
        total_stars += repo.get("stargazers_count", 0)

        if repo.get("language"):
            languages.add(repo["language"])
        
        if repo.get("updated_at"):
            active_repos += 1
        
    return {
        "public_repos": user_data.get("public_repos", 0),
        "followers" : user_data.get("followers", 0),
        "total_stars": total_stars,
        "languages": list(languages),
        "active_repos": active_repos
    }