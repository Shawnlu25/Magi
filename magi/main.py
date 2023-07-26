import openai
import chromadb
import os
from config import load_config
from memory import DialogueBufferMemory
from common import MessageRole, Message
from pathlib import Path

COMPANION_PROMPT = """
Your goal is to be a companion that I can trust completely. We are going to have conversations from time to time about a variety of topics, including but not limited to my personal life, my social network, my work, my job, my education, my family, important events happening in the world, and so on. 

Follow the instructions below:
1. Be a good listener.
2. Reply in less than 150 characters.
3. Mimic a real conversation between human friends.
4. Recognize my emotions and respond accordingly.
5. Your name is Magi.
6. Ask me questions if you need more information to facilitate a good conversation.
7. Restrict the number of questions to one per reply.

You should be able to utilize knowledge about me provided to you in the context, in order to reply in a personal way. You can omit it if the information is not helpful.
"""

def main():
    # load config and get openai api key
    config_path = Path.home() / ".magi/config.yaml"
    config = load_config(config_path)
    OPENAI_API_KEY = config.get("openai_api_key", "")

    # todo : need to initialize open ai llm in a proper way
    openai_ef = chromadb.utils.embedding_functions.OpenAIEmbeddingFunction(
                    api_key=OPENAI_API_KEY,
                    model_name="text-embedding-ada-002"
                )
    #chroma_client = chromadb.Client()
    #index = chroma_client.create_collection(name="test", embedding_function=openai_ef)

    conversation = []
    save_path = Path.home() / ".magi/dialogues"
    dialogue_mem = DialogueBufferMemory(save_path)

    dialogue_mem.new_session()

    while True:
        query = input("> ")
        if query == "exit":
            break
        
        dialogue_mem.append(Message(MessageRole.USER, query))
        messages = [Message(MessageRole.SYSTEM, COMPANION_PROMPT)] + dialogue_mem.get_context()

        print(messages)

        reply = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages = to_openai_format(messages),
        )

        reply = reply.choices[0].message.content.strip()

        print(reply)

        dialogue_mem.append(Message(MessageRole.ASSISTANT, reply))

    dialogue_mem.end_session()

def to_openai_format(messages):
    return [{"role": message.role.value, "content": message.content} for message in messages]


def initialize_workspace():
    # 1. Check existance of ~/.magi/ and mkdir if necessary

    # 2. Initialize config.yaml
    pass

if __name__ == '__main__':
    main()