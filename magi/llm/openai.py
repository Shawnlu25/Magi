from base import BaseLlm
from typing import List, Dict
from common import Message

class OpenAILlm(BaseLlm):
    
    def __init__(self, ) -> None:
        super().__init__()

    def _prepare_messages(self, messages: List[Message]) -> List[Dict]:
        raise NotImplementedError

    def chat_completion(self, messages : List[Message]):
        raise NotImplementedError
    
    def completion(self, prompt: str):
        raise NotImplementedError