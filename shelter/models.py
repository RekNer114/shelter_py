from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ShelterEntry:
    name : str
    value: str
    type : str
    filename: str | None=None
    created_at : str = field(default_factory=lambda: datetime.now().isoformat())