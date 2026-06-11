class LeetCodeFeatureExtractor:
    def __init__(self):
        pass

    def extract(self, raw_data: dict) -> dict:
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
            features["dp_strength"] = self._extract_tag(tag_data, "Dynamic Programming")
            features["graph_strength"] = self._extract_tag(tag_data, "Graphs")
            features["greedy_strength"] = self._extract_tag(tag_data, "Greedy")
        except Exception:
            features["dp_strength"] = 0
            features["graph_strength"] = 0
            features["greedy_strength"] = 0
        
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
            progress = raw_data.get("progress", {}).get("matchedUser", {}).get("submitStats", {}).get("acSubmissionNum", [])

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
    def _extract_tag(self, tag_data, tag_name):
        for level in ["advanced", "intermediate", "fundamental"]:
            for item in tag_data.get(level, []):
                if item.get("tagName") == tag_name:
                    return item.get("problemsSolved", 0)
        return 0