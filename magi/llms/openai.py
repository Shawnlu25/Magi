import openai

from .base import BaseLlm
from typing import List, Dict
from magi.common import Message, MessageRole

class OpenAILlm(BaseLlm):
    
    def __init__(self, openai_api_key: str, model: str = "gpt-3.5-turbo-0613") -> None:
        super().__init__()
        self._openai_api_key = openai_api_key
        self._model = model
        assert self._openai_api_key != "", "OpenAILlm: openai_api_key is empty"
        assert self._model != "", "OpenAILlm: model is empty"

    def _prepare_messages(self, messages: List[Message]) -> List[Dict]:
        return [{"role": message.role.value, "content": message.content} for message in messages]

    def chat_completion(self, messages: List[Message]) -> Message:
        messages = self._prepare_messages(messages)

        result = openai.ChatCompletion.create(
            api_key = self._openai_api_key,
            model=self._model,
            messages = messages,
        )
        
        reply_message = result.choices[0].message
        if reply_message.role == "assistant":
            return Message(MessageRole.ASSISTANT, reply_message.content.strip())
        if reply_message.role == "function":
            return Message(MessageRole.FUNCTION, reply_message.content.strip())
        
        raise ValueError(f"OpenAILlm: unexpected role during chat completion: {reply_message.role}")

    
    def completion(self, prompt: str):
        raise NotImplementedError