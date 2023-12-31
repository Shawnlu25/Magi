from config import *
from memory import DialogueBufferMemory
from common import MessageRole, Message
from llms import get_llm
from pathlib import Path
import asyncio

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
8. Be concise on "small talk"s.

You should be able to utilize knowledge about me provided to you in the context, in order to reply in a personal way. You can omit it if the information is not helpful.
"""

SUMMERIZATION_PROMPT = """
Read the following dialogue between the user and assistant:
{dialogue}
Now answer the following questions: 
1. What information do you find out about the user?
2. What was the conversation about? Summarize in one sentence.

Reply in a format such as the following. Fill in content only between <>s.:
[facts]
* <user fact 1>
* <user fact 2>
* <user fact>
...
* <user fact>
[summary]
<summary goes here>
"""

def main():
    # load config and get openai api key
    initialize_workspace_paths()
    config = load_config()
    llms_config = config["llms"]
    agent_config = config["agents"]["dialogue_agent"]

    # Load agent llm
    llm_config = llms_config.get(agent_config["llm"], None)
    if llm_config is None:
        raise ValueError(f"Unknown llm: {agent_config['llm']}")
    llm = get_llm(llm_config["type"], **llm_config["params"])

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

    print("Total usage: " + str(llm.total_usage))

    prompt = SUMMERIZATION_PROMPT.format(dialogue = "\n".join([str(m) for m in dialogue_mem.get_context()]))
    reply, usage = llm.chat_completion([Message(MessageRole.SYSTEM, prompt)])
    print("SUMMARY")
    print(reply)
    dialogue_mem.end_session()

if __name__ == '__main__':
    main()