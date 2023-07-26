from abc import ABC
from typing import List
from magi.common import Message

class BaseLlm(ABC):
    
    def chat_completion(self, messages : List[Message]):
        raise NotImplementedError
    
    def completion(self, prompt: str):
        raise NotImplementedError
