"""
LightRAG Evaluation Module

RAGAS-based evaluation framework for assessing RAG system quality.

Usage:
    from lightrag.evaluation import RAGEvaluator

    evaluator = RAGEvaluator()
    results = await evaluator.run()

Note: RAGEvaluator is imported lazily to avoid import errors
when ragas/datasets are not installed.
"""

__all__ = ["RAGEvaluator"]

# pylint: disable  MC8yOmFIVnBZMlhsaUpqbWxvYzZSa05LWVE9PTpiMDYxYmU2MQ==

def __getattr__(name):
    """Lazy import to avoid dependency errors when ragas is not installed."""
    if name == "RAGEvaluator":
        from .eval_rag_quality import RAGEvaluator
# fmt: off  MS8yOmFIVnBZMlhsaUpqbWxvYzZSa05LWVE9PTpiMDYxYmU2MQ==

        return RAGEvaluator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
