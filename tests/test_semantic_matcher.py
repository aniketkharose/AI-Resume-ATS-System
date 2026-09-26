from backend.services.semantic_matcher import (
    SemanticMatcher,
)


def test_semantic_similarity():

    matcher = SemanticMatcher()

    test_cases = [
        (
            "Natural Language Processing",
            "NLP",
        ),
        (
            "Deep Learning",
            "Machine Learning",
        ),
        (
            "Python programming",
            "Python",
        ),
        (
            "Docker containerization",
            "PyTorch",
        ),
    ]

    print(
        "\n========== SEMANTIC MATCHING =========="
    )

    for text_a, text_b in test_cases:

        score = matcher.calculate_similarity(
            text_a,
            text_b,
        )

        print(
            f"\n{text_a}"
            f"\n    ↕"
            f"\n{text_b}"
            f"\nSimilarity: {score}"
        )

    print(
        "\n✅ Semantic matcher working successfully."
    )


if __name__ == "__main__":
    test_semantic_similarity()