def github_score(features):
    score = 0

    score += min(features["public_repos"], 20)  # Max 20 points for public repos

    score += min(features["followers"] * 0.2, 20)   # Max 20 points for followers

    score += min(features["total_stars"] * 0.05, 30) # Max 30 points for stars

    score += min(features["active_repos"] * 2, 30) # Max 30 points for active repos

    return round(min(score, 100), 2)