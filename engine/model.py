from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid

@dataclass
class Clip:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    pinned: bool = False
    source_app: Optional[str] = None
    type: str = "text"  # text, image, file (for future)
    tags: Optional[List[str]] = field(default_factory=list)
