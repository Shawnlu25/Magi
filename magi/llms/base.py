from abc import ABC
from typing import List
from magi.common import Message

class BaseLlm(ABC):
    def __init__(self):
        pass
    
    def chat_completion(self, messages : List[Message]) -> Message:
        raise NotImplementedError
    
    def completion(self, prompt: str):
        raise NotImplementedError

