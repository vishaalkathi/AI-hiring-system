from backend.app.services.job_matching_engine import JobMatchingEngine
from backend.app.models.job import Job


# fake candidate (mimics combined_features object/dict)
class FakeCandidate:
    def __init__(self):
        self.combined_features = type("obj", (), {
            "total_solved": 200,
            "streak": 30,
            "active_days": 100,
            "repo_count": 15,
            "github_stars": 5,
            "skill_stats": {
                "dynamic_programming": 20,
                "graph_theory": 10,
                "greedy": 15
            }
        })


candidate = FakeCandidate()

job = Job(
    title="SDE Intern",
    description="Backend role",
    required_skills={
        "dynamic_programming": 10,
        "graph_theory": 8,
        "greedy": 5
    },
    min_dsa_score=50,
    min_github_score=5
)

engine = JobMatchingEngine()

result = engine.compute_match(candidate, job)

print(result)