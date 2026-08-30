import numpy as np

from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIG
# ============================================================

MODEL_NAME = "all-MiniLM-L6-v2"


# ============================================================
# SEMANTIC FEATURE ENGINEER
# ============================================================

class SemanticFeatureEngineer:
    """
    Generates semantic similarity features between:

        candidate resume
        job description

    Uses Sentence Transformers embeddings.
    """

    def __init__(
        self,
        model_name: str = MODEL_NAME
    ):

        print(
            f"Loading semantic model: {model_name}"
        )

        self.model = SentenceTransformer(
            model_name
        )

    # --------------------------------------------------------
    # Encode text
    # --------------------------------------------------------

    def encode(
        self,
        texts
    ):

        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )

    # --------------------------------------------------------
    # Cosine similarity
    # --------------------------------------------------------

    @staticmethod
    def cosine_similarity(
        resume_embedding,
        job_embedding
    ):

        return float(
            np.dot(
                resume_embedding,
                job_embedding
            )
        )

    # --------------------------------------------------------
    # Generate features
    # --------------------------------------------------------

    def transform(
        self,
        resumes,
        job_descriptions
    ):

        print(
            "Generating resume embeddings..."
        )

        resume_embeddings = self.encode(
            resumes
        )

        print(
            "Generating job description embeddings..."
        )

        job_embeddings = self.encode(
            job_descriptions
        )

        similarities = []

        for resume_embedding, job_embedding in zip(
            resume_embeddings,
            job_embeddings
        ):

            similarity = self.cosine_similarity(
                resume_embedding,
                job_embedding
            )

            similarities.append(
                similarity
            )

        return np.array(
            similarities
        )