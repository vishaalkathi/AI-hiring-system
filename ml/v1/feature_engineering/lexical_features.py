import re

import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer


# ============================================================
# LEXICAL FEATURE ENGINEER
# ============================================================

class LexicalFeatureEngineer:
    """
    Generates lexical similarity features between
    resumes and job descriptions.

    Uses TF-IDF and word overlap.
    """

    def __init__(
        self,
        max_features: int = 5000
    ):

        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words="english",
            ngram_range=(1, 2)
        )

    # --------------------------------------------------------
    # Tokenization
    # --------------------------------------------------------

    @staticmethod
    def tokenize(text):

        if not isinstance(text, str):
            return set()

        return set(
            re.findall(
                r"\b[a-zA-Z][a-zA-Z0-9+#.-]*\b",
                text.lower()
            )
        )

    # --------------------------------------------------------
    # Word overlap
    # --------------------------------------------------------

    def word_overlap(
        self,
        resume,
        job_description
    ):

        resume_words = self.tokenize(
            resume
        )

        job_words = self.tokenize(
            job_description
        )

        if not job_words:
            return 0.0

        intersection = (
            resume_words &
            job_words
        )

        return (
            len(intersection)
            /
            len(job_words)
        )

    # --------------------------------------------------------
    # TF-IDF similarity
    # --------------------------------------------------------

    def tfidf_similarity(
        self,
        resumes,
        job_descriptions
    ):

        combined_text = (
            list(resumes)
            +
            list(job_descriptions)
        )

        self.vectorizer.fit(
            combined_text
        )

        resume_vectors = (
            self.vectorizer.transform(
                resumes
            )
        )

        job_vectors = (
            self.vectorizer.transform(
                job_descriptions
            )
        )

        similarities = []

        for resume_vector, job_vector in zip(
            resume_vectors,
            job_vectors
        ):

            similarity = (
                resume_vector @
                job_vector.T
            ).toarray()[0][0]

            similarities.append(
                float(similarity)
            )

        return np.array(
            similarities
        )

    # --------------------------------------------------------
    # Transform
    # --------------------------------------------------------

    def transform(
        self,
        resumes,
        job_descriptions
    ):

        print(
            "Generating TF-IDF similarities..."
        )

        tfidf_scores = (
            self.tfidf_similarity(
                resumes,
                job_descriptions
            )
        )

        print(
            "Generating lexical word overlap..."
        )

        overlap_scores = [

            self.word_overlap(
                resume,
                job
            )

            for resume, job
            in zip(
                resumes,
                job_descriptions
            )

        ]

        return {

            "tfidf_similarity":
                tfidf_scores,

            "word_overlap":
                np.array(
                    overlap_scores
                )
        }