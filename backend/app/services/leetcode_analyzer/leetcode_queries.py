# backend/app/services/leetcode_analyzer/leetcode_queries.py


LEETCODE_QUERIES = {
    # ----------------------------
    # 1. LANGUAGE STATS
    # ----------------------------
    "languageStats": {
        "query": """
        query languageStats($username: String!) {
            matchedUser(username: $username) {
                languageProblemCount {
                    languageName
                    problemsSolved
                }
            }
        }
        """,
        "variables": lambda username: {
            "username": username
        }
    },

    # ----------------------------
    # 2. SKILL / TOPIC STATS
    # ----------------------------
    "skillStats": {
        "query": """
        query skillStats($username: String!) {
            matchedUser(username: $username) {
                tagProblemCounts {
                    advanced {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                    intermediate {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                    fundamental {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                }
            }
        }
        """,
        "variables": lambda username: {
            "username": username
        }
    },

    # ----------------------------
    # 3. CONTEST RANKING + HISTORY
    # ----------------------------
    "contestInfo": {
        "query": """
        query userContestRankingInfo($username: String!) {
            userContestRanking(username: $username) {
                attendedContestsCount
                rating
                globalRanking
                totalParticipants
                topPercentage
                badge {
                    name
                }
            }

            userContestRankingHistory(username: $username) {
                attended
                trendDirection
                problemsSolved
                totalProblems
                finishTimeInSeconds
                rating
                ranking
                contest {
                    title
                    startTime
                }
            }
        }
        """,
        "variables": lambda username: {
            "username": username
        }
    },

    # ----------------------------
    # 4. PROBLEM PROGRESS (AC / FAIL / DIFFICULTY)
    # ----------------------------
    "progress": {
        "query": """
        query userProfileUserQuestionProgressV2($userSlug: String!) {
            userProfileUserQuestionProgressV2(userSlug: $userSlug) {
                numAcceptedQuestions {
                    count
                    difficulty
                }
                numFailedQuestions {
                    count
                    difficulty
                }
                numUntouchedQuestions {
                    count
                    difficulty
                }
                userSessionBeatsPercentage {
                    difficulty
                    percentage
                }
                totalQuestionBeatsPercentage
            }
        }
        """,
        "variables": lambda username: {
            "userSlug": username
        }
    },

    # ----------------------------
    # 5. SUBMISSION STATS (TOTAL + ACCEPTED)
    # ----------------------------
    "submissionStats": {
        "query": """
        query userSessionProgress($username: String!) {
            allQuestionsCount {
                difficulty
                count
            }
            matchedUser(username: $username) {
                submitStats {
                    acSubmissionNum {
                        difficulty
                        count
                        submissions
                    }
                    totalSubmissionNum {
                        difficulty
                        count
                        submissions
                    }
                }
            }
        }
        """,
        "variables": lambda username: {
            "username": username
        }
    },

    # ----------------------------
    # 6. ACTIVITY CALENDAR (STREAK + HEATMAP)
    # ----------------------------
    "calendar": {
        "query": """
        query userProfileCalendar($username: String!, $year: Int) {
            matchedUser(username: $username) {
                userCalendar(year: $year) {
                    activeYears
                    streak
                    totalActiveDays
                    submissionCalendar
                    dccBadges {
                        timestamp
                        badge {
                            name
                            icon
                        }
                    }
                }
            }
        }
        """,
        "variables": lambda username: {
            "username": username,
            "year": None
        }
    }
}