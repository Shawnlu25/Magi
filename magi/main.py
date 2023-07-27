from config import *
from memory import DialogueBufferMemory
from common import MessageRole, Message
from llms import OpenAILlm
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
    initialize_workspace_paths()
    config = load_config()

    # Load LLM
    llm = OpenAILlm(config.get("openai_api_key", ""), config.get("openai_default_model", ""))

    # Start new session
    dialogue_mem = DialogueBufferMemory(DIALOGUE_SAVE_PATH)
    dialogue_mem.new_session()

    while True:
        query = input("USER > ")
        if query == "exit":
            break
        
        dialogue_mem.append(Message(MessageRole.USER, query))
        messages = [Message(MessageRole.SYSTEM, COMPANION_PROMPT)] + dialogue_mem.get_context()

        reply, usage = llm.chat_completion(messages)
        print("\033[2m"+str(usage)+"\033[0m")
        print("ASSISTANT: " + reply.content)
        dialogue_mem.append(reply)

    dialogue_mem.end_session()

if __name__ == '__main__':
    main()