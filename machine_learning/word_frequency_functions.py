"""
Word Frequency Functions

Text processing utilities for NLP: word counting, TF-IDF,
bag of words, and document similarity.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/word_frequency_functions.py
"""

import math
from collections import Counter


def word_frequency(text: str) -> dict[str, int]:
    """
    Count word frequencies in text.

    >>> word_frequency("the cat sat on the mat")
    {'the': 2, 'cat': 1, 'sat': 1, 'on': 1, 'mat': 1}
    """
    words = text.lower().split()
    return dict(Counter(words))


def term_frequency(term: str, document: str) -> float:
    """
    TF: frequency of term in document / total terms in document.

    >>> term_frequency("the", "the cat sat on the mat")
    0.3333333333333333
    """
    words = document.lower().split()
    return words.count(term.lower()) / len(words)


def inverse_document_frequency(term: str, documents: list[str]) -> float:
    """
    IDF: log(total documents / documents containing term).

    >>> docs = ["the cat sat", "the dog ran", "a bird flew"]
    >>> round(inverse_document_frequency("the", docs), 4)
    0.4055
    >>> round(inverse_document_frequency("bird", docs), 4)
    1.0986
    """
    n_docs = len(documents)
    doc_count = sum(1 for doc in documents if term.lower() in doc.lower().split())
    if doc_count == 0:
        return 0.0
    return math.log(n_docs / doc_count)


def tf_idf(term: str, document: str, documents: list[str]) -> float:
    """
    TF-IDF: Term Frequency * Inverse Document Frequency.

    >>> docs = ["the cat sat", "the dog ran", "a bird flew"]
    >>> round(tf_idf("cat", "the cat sat", docs), 4)
    0.3662
    """
    return term_frequency(term, document) * inverse_document_frequency(
        term, documents
    )


def bag_of_words(documents: list[str]) -> tuple[list[str], list[list[int]]]:
    """
    Create bag-of-words representation.

    Returns (vocabulary, document_vectors).

    >>> vocab, vectors = bag_of_words(["the cat", "the dog", "a cat"])
    >>> 'cat' in vocab
    True
    >>> len(vectors) == 3
    True
    """
    # Build vocabulary
    vocab_set: set[str] = set()
    for doc in documents:
        vocab_set.update(doc.lower().split())
    vocab = sorted(vocab_set)

    # Create vectors
    vectors = []
    for doc in documents:
        words = doc.lower().split()
        counter = Counter(words)
        vector = [counter.get(word, 0) for word in vocab]
        vectors.append(vector)

    return vocab, vectors


def document_similarity(doc1: str, doc2: str) -> float:
    """
    Cosine similarity between two documents using bag-of-words.

    >>> round(document_similarity("the cat sat", "the cat ran"), 4)
    0.6667
    >>> round(document_similarity("hello world", "hello world"), 4)
    1.0
    """
    vocab, vectors = bag_of_words([doc1, doc2])
    v1 = vectors[0]
    v2 = vectors[1]

    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))

    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def n_grams(text: str, n: int = 2) -> list[str]:
    """
    Generate n-grams from text.

    >>> n_grams("the cat sat on the mat", 2)
    ['the cat', 'cat sat', 'sat on', 'on the', 'the mat']
    >>> n_grams("hello world", 1)
    ['hello', 'world']
    """
    words = text.lower().split()
    return [" ".join(words[i : i + n]) for i in range(len(words) - n + 1)]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- Word Frequency Functions Demo ---")
    documents = [
        "machine learning is great",
        "deep learning is a subset of machine learning",
        "natural language processing uses machine learning",
        "computer vision is another field of AI",
    ]

    print("Documents:")
    for i, doc in enumerate(documents):
        print(f"  {i}: {doc}")

    # Word frequency
    print(f"\nWord frequency (doc 0): {word_frequency(documents[0])}")

    # TF-IDF for key terms
    print("\nTF-IDF scores:")
    for term in ["machine", "learning", "deep", "vision"]:
        scores = [round(tf_idf(term, doc, documents), 4) for doc in documents]
        print(f"  '{term}': {scores}")

    # Document similarity
    print("\nDocument similarity matrix:")
    for i in range(len(documents)):
        sims = [round(document_similarity(documents[i], documents[j]), 3) for j in range(len(documents))]
        print(f"  Doc {i}: {sims}")
