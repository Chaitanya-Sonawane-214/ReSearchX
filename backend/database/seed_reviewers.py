from database.connection import SessionLocal
from models.reviewer import Reviewer


REVIEWERS = [
    {
        "id": "rev-ananya-sharma",
        "name": "Dr. Ananya Sharma",
        "expertise": ["Machine Learning", "Deep Learning", "NLP"],
        "domains": [
            "Artificial Intelligence / Machine Learning",
            "Natural Language Processing",
        ],
        "publications": 47,
        "workload": "LOW",
        "coi": False,
        "bio": (
            "Associate Professor of Computer Science focusing on "
            "representation learning and NLP."
        ),
    },
    {
        "id": "rev-rahul-mehta",
        "name": "Dr. Rahul Mehta",
        "expertise": ["Computer Vision", "Deep Learning", "Multi-Agent Systems"],
        "domains": [
            "Artificial Intelligence / Machine Learning",
            "Computer Vision",
        ],
        "publications": 38,
        "workload": "MEDIUM",
        "coi": False,
        "bio": (
            "Research scientist specializing in vision architectures "
            "and multi-agent coordination."
        ),
    },
    {
        "id": "rev-sara-iyer",
        "name": "Dr. Sara Iyer",
        "expertise": ["Distributed Systems", "Cloud Computing", "Networking"],
        "domains": ["Networking / Systems"],
        "publications": 29,
        "workload": "LOW",
        "coi": False,
        "bio": (
            "Systems researcher with a focus on distributed and edge "
            "computing architectures."
        ),
    },
    {
        "id": "rev-david-chen",
        "name": "Dr. David Chen",
        "expertise": ["Bioinformatics", "Clinical ML", "Healthcare Analytics"],
        "domains": ["Bioinformatics / Healthcare"],
        "publications": 52,
        "workload": "HIGH",
        "coi": False,
        "bio": (
            "Faculty researcher applying machine learning to clinical "
            "and genomic datasets."
        ),
    },
    {
        "id": "rev-meera-nair",
        "name": "Dr. Meera Nair",
        "expertise": ["Robotics", "Control Systems", "Sensor Fusion"],
        "domains": ["Robotics"],
        "publications": 24,
        "workload": "MEDIUM",
        "coi": False,
        "bio": (
            "Robotics lab lead working on autonomous navigation "
            "and sensor fusion."
        ),
    },
    {
        "id": "rev-omar-farouk",
        "name": "Dr. Omar Farouk",
        "expertise": ["Cybersecurity", "Applied Cryptography", "Systems Security"],
        "domains": ["Security"],
        "publications": 33,
        "workload": "LOW",
        "coi": False,
        "bio": (
            "Security researcher focused on applied cryptography "
            "and intrusion detection."
        ),
    },
    {
        "id": "rev-lena-petrova",
        "name": "Dr. Lena Petrova",
        "expertise": [
            "Sustainability Modeling",
            "Environmental Data Science",
            "Time-Series ML",
        ],
        "domains": [
            "Environmental / Sustainability",
            "Artificial Intelligence / Machine Learning",
        ],
        "publications": 31,
        "workload": "MEDIUM",
        "coi": False,
        "bio": (
            "Applies machine learning to climate and environmental "
            "forecasting problems."
        ),
    },
    {
        "id": "rev-james-okoro",
        "name": "Dr. James Okoro",
        "expertise": [
            "Machine Learning",
            "Reinforcement Learning",
            "Optimization",
        ],
        "domains": ["Artificial Intelligence / Machine Learning"],
        "publications": 41,
        "workload": "HIGH",
        "coi": False,
        "bio": (
            "Works on reinforcement learning and large-scale "
            "optimization methods."
        ),
    },
]


def seed_reviewers():
    db = SessionLocal()

    try:
        for reviewer_data in REVIEWERS:
            reviewer = Reviewer(**reviewer_data)

            # Update existing reviewer or insert new reviewer
            existing = db.get(Reviewer, reviewer_data["id"])

            if existing:
                for key, value in reviewer_data.items():
                    setattr(existing, key, value)
            else:
                db.add(reviewer)

        db.commit()

        print(f"Successfully seeded {len(REVIEWERS)} reviewers!")

    except Exception as e:
        db.rollback()
        print("Failed to seed reviewers!")
        print(e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_reviewers()