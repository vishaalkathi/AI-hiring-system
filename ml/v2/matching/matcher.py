# ============================================================
# AI-HIRE V2
# DETERMINISTIC MATCHING ENGINE
# ============================================================

from ml.matching.ontology import (
    normalize_skill,
    normalize_skills,
    language_similarity
)


ROLE_FAMILY_COMPATIBILITY = {

    "software": {
        "software": 1.0,
        "devops_cloud": 0.75,
        "mobile": 0.65,
        "qa": 0.55,
        "database": 0.50,
        "data": 0.45,
        "ml_ai": 0.40,
    },

    "data": {
        "data": 1.0,
        "ml_ai": 0.75,
        "database": 0.70,
        "software": 0.45,
        "business": 0.40,
    },

    "ml_ai": {
        "ml_ai": 1.0,
        "data": 0.80,
        "software": 0.45,
        "robotics": 0.50,
    },

    "devops_cloud": {
        "devops_cloud": 1.0,
        "software": 0.75,
        "database": 0.55,
        "security": 0.50,
    },

    "mobile": {
        "mobile": 1.0,
        "software": 0.70,
        "ar_vr": 0.55,
        "game": 0.45,
    },

    "database": {
        "database": 1.0,
        "data": 0.70,
        "devops_cloud": 0.55,
        "software": 0.50,
    },

    "qa": {
        "qa": 1.0,
        "software": 0.55,
        "devops_cloud": 0.45,
    },

    "security": {
        "security": 1.0,
        "devops_cloud": 0.55,
        "software": 0.45,
    },

    "robotics": {
        "robotics": 1.0,
        "ml_ai": 0.65,
        "software": 0.55,
    },

    "game": {
        "game": 1.0,
        "ar_vr": 0.65,
        "software": 0.50,
    },

    "ar_vr": {
        "ar_vr": 1.0,
        "game": 0.65,
        "mobile": 0.50,
    }
}


def role_compatibility(
    candidate_family,
    job_family
):

    if candidate_family == job_family:
        return 1.0

    return ROLE_FAMILY_COMPATIBILITY.get(
        candidate_family,
        {}
    ).get(job_family, 0.0)


def skill_match(
    candidate_skills,
    required_skills
):

    candidate_skills = normalize_skills(
        candidate_skills
    )

    required_skills = normalize_skills(
        required_skills
    )

    if not required_skills:
        return 0.5, [], []


    matched = []
    missing = []

    total_score = 0.0

    for required in required_skills:

        best_score = 0.0
        best_candidate = None

        # Exact/general match
        for candidate in candidate_skills:

            if candidate == required:

                best_score = 1.0
                best_candidate = candidate
                break

        # Language relationship
        if best_score == 0:

            for candidate in candidate_skills:

                similarity = language_similarity(
                    candidate,
                    required
                )

                if similarity > best_score:

                    best_score = similarity
                    best_candidate = candidate


        if best_score > 0:

            total_score += best_score

            matched.append({
                "required": required,
                "candidate": best_candidate,
                "score": round(
                    best_score,
                    3
                )
            })

        else:

            missing.append(required)


    score = (
        total_score /
        len(required_skills)
    )

    return score, matched, missing


def preferred_skill_score(
    candidate_skills,
    preferred_skills
):

    if not preferred_skills:
        return 0.0

    candidate_skills = normalize_skills(
        candidate_skills
    )

    preferred_skills = normalize_skills(
        preferred_skills
    )

    matched = 0

    for skill in preferred_skills:

        if skill in candidate_skills:
            matched += 1

    return matched / len(preferred_skills)


def experience_score(
    candidate_experience,
    min_experience,
    max_experience
):

    if candidate_experience is None:
        return 0.5

    if min_experience is None:
        return 1.0

    candidate_experience = float(
        candidate_experience
    )

    min_experience = float(
        min_experience
    )

    if candidate_experience >= min_experience:

        if (
            max_experience is None
            or candidate_experience <= max_experience
        ):
            return 1.0

        return 0.9

    # Candidate is below required experience
    difference = (
        min_experience -
        candidate_experience
    )

    if difference <= 1:
        return 0.7

    if difference <= 2:
        return 0.5

    return 0.2


def match_candidate_to_job(
    candidate,
    job
):

    candidate_skills = (
        candidate.get("skills", [])
        + candidate.get(
            "programming_languages",
            []
        )
        + candidate.get(
            "frameworks",
            []
        )
        + candidate.get(
            "databases",
            []
        )
        + candidate.get(
            "cloud",
            []
        )
        + candidate.get(
            "devops",
            []
        )
        + candidate.get(
            "concepts",
            []
        )
    )


    required_skills = (
        job.get("required_skills", [])
        + job.get(
            "programming_languages",
            []
        )
        + job.get(
            "frameworks",
            []
        )
        + job.get(
            "databases",
            []
        )
        + job.get(
            "cloud",
            []
        )
        + job.get(
            "devops",
            []
        )
        + job.get(
            "concepts",
            []
        )
    )


    preferred_skills = (
        job.get("preferred_skills", [])
    )


    required_score, matched, missing = (
        skill_match(
            candidate_skills,
            required_skills
        )
    )


    preferred_score = preferred_skill_score(
        candidate_skills,
        preferred_skills
    )


    role_score = role_compatibility(
        candidate.get("role_family", "other"),
        job.get("role_family", "other")
    )


    exp_score = experience_score(
        candidate.get("experience_years"),
        job.get("min_experience_years"),
        job.get("max_experience_years")
    )


    # --------------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------------

    score = (
        required_score * 0.55
        + preferred_score * 0.10
        + role_score * 0.20
        + exp_score * 0.15
    )


    score = round(
        score * 100,
        2
    )


    label = score_to_label(score)


    reason = generate_reason(
        score=score,
        role_score=role_score,
        required_score=required_score,
        preferred_score=preferred_score,
        exp_score=exp_score,
        matched=matched,
        missing=missing
    )


    return {
        "score": score,
        "label": label,

        "role_score": round(
            role_score * 100,
            2
        ),

        "required_skill_score": round(
            required_score * 100,
            2
        ),

        "preferred_skill_score": round(
            preferred_score * 100,
            2
        ),

        "experience_score": round(
            exp_score * 100,
            2
        ),

        "matched_skills": matched,
        "missing_skills": missing,

        "reason": reason
    }


def score_to_label(score):

    if score >= 85:
        return 5

    if score >= 70:
        return 4

    if score >= 55:
        return 3

    if score >= 40:
        return 2

    if score >= 25:
        return 1

    return 0


def generate_reason(
    score,
    role_score,
    required_score,
    preferred_score,
    exp_score,
    matched,
    missing
):

    reasons = []


    if required_score >= 0.8:
        reasons.append(
            "strong alignment with required skills"
        )

    elif required_score >= 0.5:
        reasons.append(
            "partial alignment with required skills"
        )

    else:
        reasons.append(
            "limited alignment with required skills"
        )


    if role_score >= 0.8:
        reasons.append(
            "strong role-family alignment"
        )

    elif role_score >= 0.5:
        reasons.append(
            "related role background"
        )

    else:
        reasons.append(
            "limited role-family alignment"
        )


    if exp_score >= 0.9:
        reasons.append(
            "experience level aligns well"
        )

    elif exp_score < 0.5:
        reasons.append(
            "experience level is below the requirement"
        )


    if missing:

        missing_preview = ", ".join(
            missing[:5]
        )

        reasons.append(
            f"missing required skills: {missing_preview}"
        )


    return "; ".join(reasons)