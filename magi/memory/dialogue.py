from typing import List
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path

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


class DialogueSession():
    """A dialogue session, consisting of a list of messages."""

    def __init__(self):
        self.messages = []
        self.start_time = datetime.now().isoformat()

    def __iter__(self):
        return iter(self.messages)

    def __len__(self) -> int:
        len(self.messages)

    def append(self, message: Message):
        self.messages.append(message)

    def read_from_tail(self, n: int = 1) -> List[Message]:
        return self.messages[-n:]

    def dump_json(self):
        return json.dumps({
            "messages": [asdict(message) for message in self.messages],
            "start_time": self.start_time
        })
    
    def load_json(self, json_str):
        json_dict = json.loads(json_str)
        self.messages = [Message(**message) for message in json_dict["messages"]]
        self.start_time = json_dict["start_time"]

    @staticmethod
    def from_json(json_str):
        dialogue_session = DialogueSession()
        dialogue_session.load_json(json_str)
        return dialogue_session
    

class DialogueBufferMemory():
    """A memory module that provides dialogue history as context for subsequent LLM operations."""

    def __init__(self, save_path: Path, max_context_size: int):
        self.max_context_size = max_context_size
        self.session = None
        
    def new_session(self):
        raise NotImplementedError()

    def end_session(self):
        raise NotImplementedError()
    
    def get_context(self):
        raise NotImplementedError()
    