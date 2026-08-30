# ============================================================
# ROLE TAXONOMY
# ============================================================

ROLE_FAMILIES = {

    "software": [
        "software engineer",
        "software developer",
        "software development engineer",
        "backend developer",
        "backend engineer",
        "frontend developer",
        "frontend engineer",
        "full stack developer",
        "full stack engineer",
        "application developer",
        "application engineer",
        "web developer",
        "web engineer",
        "systems software engineer",
        "java developer",
        "python developer",
        "c++ developer",
        "c developer",
        "dot net developer",
        ".net developer",
    ],

    "data": [
        "data scientist",
        "data analyst",
        "data engineer",
        "data developer",
        "analytics engineer",
        "business intelligence analyst",
        "bi developer",
        "data analytics",
    ],

    "ml_ai": [
        "machine learning engineer",
        "machine learning developer",
        "machine learning scientist",
        "ai engineer",
        "ai developer",
        "artificial intelligence engineer",
        "artificial intelligence developer",
        "ai researcher",
        "research scientist",
        "deep learning engineer",
        "nlp engineer",
        "computer vision engineer",
    ],

    "devops_cloud": [
        "devops engineer",
        "cloud engineer",
        "cloud architect",
        "cloud developer",
        "site reliability engineer",
        "sre",
        "platform engineer",
        "infrastructure engineer",
        "devops developer",
        "cloud infrastructure engineer",
    ],

    "security": [
        "cybersecurity analyst",
        "cyber security analyst",
        "security analyst",
        "security engineer",
        "cybersecurity engineer",
        "information security analyst",
        "information security engineer",
        "penetration tester",
        "security consultant",
    ],

    "database": [
        "database administrator",
        "database developer",
        "database engineer",
        "sql developer",
        "database analyst",
        "database architect",
    ],

    "qa": [
        "qa engineer",
        "qa analyst",
        "test engineer",
        "software tester",
        "automation tester",
        "quality assurance engineer",
        "test automation engineer",
    ],

    "robotics": [
        "robotics engineer",
        "robotics developer",
        "robotics software engineer",
        "ros developer",
        "robotics software developer",
    ],

    "mobile": [
        "mobile app developer",
        "mobile developer",
        "android developer",
        "android engineer",
        "ios developer",
        "ios engineer",
        "mobile application developer",
    ],

    "game": [
        "game developer",
        "game programmer",
        "game engineer",
        "unity developer",
        "unity engineer",
        "unreal developer",
        "game designer",
    ],

    "ar_vr": [
        "ar developer",
        "vr developer",
        "ar/vr developer",
        "ar vr developer",
        "augmented reality developer",
        "virtual reality developer",
    ],

    "design": [
        "ux designer",
        "ui designer",
        "ui/ux designer",
        "product designer",
        "user experience designer",
    ],

    "management": [
        "product manager",
        "project manager",
        "technical product manager",
    ],

    "business": [
        "business analyst",
        "business intelligence analyst",
        "systems analyst",
    ],
}


def normalize_role(role):
    """
    Normalize a job title for role-family matching.
    """

    if role is None:
        return ""

    return (
        str(role)
        .lower()
        .strip()
    )


def get_role_family(role):
    """
    Return the most appropriate role family.

    Uses substring matching so titles such as:

        Senior Software Engineer
        Backend Software Engineer
        Java Developer

    can still be classified.
    """

    role = normalize_role(role)

    if not role:
        return "other"

    for family, roles in ROLE_FAMILIES.items():

        for known_role in roles:

            if known_role in role:
                return family

    return "other"