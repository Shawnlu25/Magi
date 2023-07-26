from abc import ABC
from typing import List

class BaseLlm(ABC):
    
    def chat_completion(self, messages):
        raise NotImplementedError
    
    def completion(self, prompt):
        raise NotImplementedError
