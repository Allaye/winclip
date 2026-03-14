"""Data model for clipboard entries."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid


@dataclass
class Clip:
    """A single clipboard entry.

    Attributes:
        id: Unique identifier.
        content: The copied text.
        timestamp: When the clip was captured.
        pinned: Whether the clip is pinned (protected from clear-all).
        source_app: Name of the application the text was copied from.
        type: Content type — ``text``, ``image``, or ``file``.
        tags: Optional list of user-defined tags.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    pinned: bool = False
    source_app: Optional[str] = None
    type: str = "text"  # text, image, file (for future)
    tags: Optional[List[str]] = field(default_factory=list)
