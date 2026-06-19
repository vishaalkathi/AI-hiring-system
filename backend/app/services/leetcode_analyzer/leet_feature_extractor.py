
def extract_features(raw_data: dict) -> dict:
    if not raw_data:
        return {"error": "No data to extract features from"}
    
    features = {}

    #LANGUAGE STATS

    try:
        lang_data = raw_data.get("languageStats", {}).get("matchedUser", {}).get("languageProblemCount", [])
        features["language_diversity"] = len(lang_data)
        features["language_list"] = [x["languageName"] for x in lang_data]

        if lang_data:
            primary = max(lang_data, key = lambda x: x["problemsSolved"])
            features["primary_language"] = primary["languageName"]
            features["primary_language_share"] = primary["problemsSolved"] / sum(x["problemsSolved"] for x in lang_data)
        else:
            features["primary_language"] = None
            features["primary_language_share"] = 0
    except Exception:
        features["language_diversity"] = 0
        features["language_list"] = []
        features["primary_language"] = None
        features["primary_language_share"] = 0

    # -------------------------
    # 2. SKILL / TAG STATS
    # -------------------------

    try: 
        tag_data = raw_data.get("skillStats", {}).get("matchedUser", {}).get("tagProblemCounts", {})

        skill_stats = extract_all_tags(tag_data)
        #normalized_features = normalize_features(skill_stats)

        features["skill_stats"] = skill_stats
        #features["normalized_features"] = normalized_features
    except Exception:
        features["skill_stats"] = {}
        #features["normalized_features"] = {}
    
    # -------------------------
    # 3. CONTEST DATA
    # -------------------------

    try:
        contest = raw_data.get("contestInfo", {}).get("userContestRanking", None)

        if contest:
            features["contest_rating"] = contest.get("rating", 0)
            features["contest_rank_percentile"] = contest.get("topPercentage", 100)
            features["contest_attended"] = contest.get("attendedContestsCount", 0)
        else:
            features["contest_rating"] = 0
            features["contest_rank_percentile"] = 100
            features["contest_attended"] = 0
    except Exception:
        features["contest_rating"] = 0
        features["contest_rank_percentile"] = 100
        features["contest_attended"] = 0
    
    # -------------------------
    # 4. PROGRESS (solved problems)
    # -------------------------

    try:
        progress = raw_data.get("submissionStats", {}).get("matchedUser", {}).get("submitStats", {}).get("acSubmissionNum", [])

        features["total_solved"] = sum(x["count"] for x in progress if x["difficulty"] in ["Easy", "Medium", "Hard"])

        breakdown = {
            x["difficulty"].lower(): x["count"]
            for x in progress
            if x["difficulty"] in ["Easy", "Medium", "Hard"]
        }

        features["easy"] = breakdown.get("easy", 0)
        features["medium"] = breakdown.get("medium", 0)
        features["hard"] = breakdown.get("hard", 0)

    except Exception:
        features["total_solved"] = 0
        features["easy"] = 0
        features["medium"] = 0
        features["hard"] = 0
    
    # -------------------------
    # 5. CONSISTENCY (calendar)
    # -------------------------

    try:
        calendar = raw_data.get("calendar", {}).get("matchedUser", {}).get("userCalendar", {})

        features["streak"] = calendar.get("streak", 0)
        features["active_days"] = calendar.get("totalActiveDays", 0)
    except Exception:
        features["streak"] = 0
        features["active_days"] = 0
    
    return features

# -------------------------
# helper function
# -------------------------
def extract_all_tags(tag_data: dict) -> dict:
    """
    Extract all LeetCode skill tags into a flat dictionary.
    """
    if not tag_data:
        return {}

    tag_features = {}

    for level in ["advanced", "intermediate", "fundamental"]:
        for item in tag_data.get(level, []):
            tag_name = item.get("tagName")
            count = item.get("problemsSolved", 0)

            if tag_name:
                key = tag_name.lower().replace(" ", "_")
                tag_features[key] = count

    return tag_features

#-----------------------------------------------------
#Fix this normalization for the ML model, we can add more rules here
#-----------------------------------------------------
def normalize_features(skill_stats: dict) -> dict:
    """
    Optional ML-friendly normalization layer.
    You can expand this later with mapping rules.
    """
    if not skill_stats:
        return {}

    # simple aliasing (you can expand this later)
    alias_map = {
        "graph_theory": "graphs",
        "breadth_first_search": "graphs",
        "depth_first_search": "graphs",
        "binary_tree": "trees",
        "binary_search_tree": "trees",
    }

    normalized = {}

    for k, v in skill_stats.items():
        key = alias_map.get(k, k)
        normalized[key] = normalized.get(key, 0) + v

    return normalized