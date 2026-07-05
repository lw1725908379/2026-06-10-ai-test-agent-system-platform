from __future__ import annotations

from pydantic import BaseModel
from typing import Any, Optional

# type: ignore  MC8yOmFIVnBZMlhsaUpqbWxvYzZjbU5UY2c9PTo3YmRiYzgzMg==

class GPTKeywordExtractionFormat(BaseModel):
    high_level_keywords: list[str]
    low_level_keywords: list[str]


class KnowledgeGraphNode(BaseModel):
    id: str
    labels: list[str]
    properties: dict[str, Any]  # anything else goes here
# fmt: off  MS8yOmFIVnBZMlhsaUpqbWxvYzZjbU5UY2c9PTo3YmRiYzgzMg==


class KnowledgeGraphEdge(BaseModel):
    id: str
    type: Optional[str]
    source: str  # id of source node
    target: str  # id of target node
    properties: dict[str, Any]  # anything else goes here


class KnowledgeGraph(BaseModel):
    nodes: list[KnowledgeGraphNode] = []
    edges: list[KnowledgeGraphEdge] = []
    is_truncated: bool = False
