import openai
import chromadb
import argparse
import yaml
from collections import deque
from typing import List, Dict, Deque
from sys import load_config, initialize_config

TASK_CREATION_PROMPT = """
You are an task creation AI that uses the result of an execution agent to create new tasks with the following objective: {objective}. The last completed task has the result: {result}. This result was based on this task description: {task_description}. These are incomplete tasks: {incomplete_task}. Based on the result, create new tasks to be completed by the AI system that do not overlap with incomplete tasks. Return the tasks as an unnumbered list, like:
    #. First task
    #. Second task
"""

TASK_EXECUTION_PROMPT = """
f"You are an AI who performs one task based on the following objective: {objective}. Your task: {task}\nResponse:
"""

TASK_PRIORITIZATION_PROMPT = """You are an task prioritization AI tasked with cleaning the formatting of and reprioritizing the following tasks: {tasks}. Consider the ultimate objective of your team:{objective}. Do not remove any tasks. Return the result as a numbered list, like:
    #. First task
    #. Second task
    Start the task list with number {next_task_id}."""


def add_task(task_list: Deque, task: Dict):
    task_list.append(task)

def task_creation_agent(objective: str, result: Dict, task_description: str, task_list: List[str]) -> Dict:
    prompt = TASK_CREATION_PROMPT.format(
        objective=objective, 
        result=result, 
        task_description=task_description, incomplete_task=", ".join([task["task"] for task in task_list])
        )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5, 
        max_tokens=200,
        top_p=1,
        frequency_penalty=0, 
        presence_penalty=0
    )
    new_tasks = response.choices[0].text.strip().split("\n")
    return [{"task": task} for task in new_tasks]

def prioritization_agent(this_task_id:int, task_list: Deque, objective: str):
    task_names = [t["task"] for t in task_list]
    next_task_id = int(this_task_id)+1
    prompt = TASK_PRIORITIZATION_PROMPT.format(
        tasks=";\n".join(task_names),
        objective=objective,
        next_task_id=next_task_id
        )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    new_tasks = response.choices[0].text.strip().split('\n')
    print(new_tasks)
    task_list = deque()
    for task_string in new_tasks:
        task_parts = task_string.strip().split(".", 1)
        if len(task_parts) == 2:
            task_id = task_parts[0].strip()
            task_name = task_parts[1].strip()
            task_list.append({"task_id": task_id, "task": task_name})

def execution_agent(objective: str, task: str, index) -> str:
    #context = context_agent(query=objective, index=index, n=5)
    prompt = TASK_EXECUTION_PROMPT.format(
        objective=objective, 
        task=task
    )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7, 
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0, 
        presence_penalty=0
    )
    return response.choices[0].text.strip()


def context_agent(query: str, index, n: int):
    results = index.query(query_texts=[query], n_results=n)
    return results



def main():
    parser = argparse.ArgumentParser(description='Magi')
    parser.add_argument('config', type=str, help='Input file')

    args = parser.parse_args()
    config = None
    with open(args.config, "r") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)
            exit(-1)

    # Prompt for objective and first task
    objective = input("\033[96m\033[1m" + "Objective > " + "\033[0m\033[0m")
    first_task = input("\033[96m\033[1m" + "First task > " + "\033[0m\033[0m")

    # Build the vector index
    openai_ef = chromadb.utils.embedding_functions.OpenAIEmbeddingFunction(
                api_key=config["openai_api_key"],
                model_name="text-embedding-ada-002"
            )
    chroma_client = chromadb.Client()
    index = chroma_client.create_collection(name="magi_temp", embedding_function=openai_ef)

    # Build task list
    task_list = deque([])
    task_id = 0
    add_task(task_list, 
             {"task_id": task_id, 
              "task": first_task})
    task_id += 1

    while True:
        if len(task_list) == 0:
            break
        
        # Print the task list
        print("\033[95m\033[1m"+"\n*****TASK LIST*****\n"+"\033[0m\033[0m")
        for t in task_list:
            print(str(t['task_id'])+": "+t['task'])
        
        # Pull the first task
        task = task_list.popleft()
        print("\033[92m\033[1m"+"\n*****NEXT TASK*****\n"+"\033[0m\033[0m")
        print(str(task['task_id'])+": "+task['task'])

        # Execute the task
        result = execution_agent(objective, task["task"], index)
        this_task_id = int(task["task_id"])
        print("\033[93m\033[1m"+"\n*****TASK RESULT*****\n"+"\033[0m\033[0m")
        print(result)

        # Task enrich?

        # Create new tasks
        new_tasks = task_creation_agent(objective, result, task["task"], task_list)
        print("\033[93m\033[1m"+"\n*****NEW TASKS*****\n"+"\033[0m\033[0m")
        print(new_tasks)
        for new_task in new_tasks:
            new_task["task_id"] = task_id
            task_id += 1
            add_task(task_list, new_task)
        
        prioritization_agent(this_task_id, task_list, objective)


if __name__ == "__main__":
    main()
