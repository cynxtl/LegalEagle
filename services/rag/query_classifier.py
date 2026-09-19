"""Forwarding module for services.rag.query_classifier."""
from backend.app.services.rag.query_classifier import (
    QueryClassification,
    LegalQueryClassifier,
    classifier,
    classify_query,
)

__all__ = [
    "QueryClassification",
    "LegalQueryClassifier",
    "classifier",
    "classify_query",
]
