import json
from typing import List
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from magi.common import Message

class DialogueSession():
    """A dialogue session, consisting of a list of messages."""

    def __init__(self):
        self.messages = []
        self.start_time = datetime.now().isoformat()
        self.uuid = str(uuid4())

    def __iter__(self):
        return iter(self.messages)

    def __len__(self) -> int:
        return len(self.messages)

    def append(self, message: Message):
        self.messages.append(message)

    def read_from_tail(self, n: int = 1) -> List[Message]:
        return self.messages[-n:]

    def to_json(self):
        return json.dumps({
            "messages": [asdict(message) for message in self.messages],
            "start_time": self.start_time,
            "uuid": self.uuid
        })
    
    def _load_json(self, json_str):
        json_dict = json.loads(json_str)
        self.messages = [Message(**message) for message in json_dict["messages"]]
        self.start_time = json_dict["start_time"]
        self.uuid = json_dict["uuid"]

    @staticmethod
    def from_json(json_str):
        dialogue_session = DialogueSession()
        dialogue_session._load_json(json_str)
        return dialogue_session
    

class DialogueBufferMemory():
    """A memory module that provides dialogue history as context for subsequent LLM operations."""

    def __init__(self, path: Path, max_context_size: int = 20):
        self.path = path
        self.max_context_size = max_context_size
        self.session = None
        self.new_session()
        
    def new_session(self):
        self.session = DialogueSession()

    def end_session(self):
        filename =self.path / f"{self.session.start_time}.{self.session.uuid}.json"
        with open(filename, "w") as f:
            f.write(self.session.to_json())
    
    def get_context(self):
        return self.session.read_from_tail(self.max_context_size)
    
    def append(self, message: Message):
        self.session.append(message)
