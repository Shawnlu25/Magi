from dataclasses import dataclass, field, asdict
from datetime import datetime
import json

@dataclass
class Message():
    """A message in a dialogue session."""
    type: str
    content: str
    timestamp : str = field(default_factory=lambda : datetime.now().isoformat())

    def dump_json(self):
        return json.dumps(asdict(self))
    
    @classmethod
    def load_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)