import sys
import json
import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent

async def run_agent(task):
    agent = Agent(
        task=task,
        llm=ChatOpenAI(model='gpt-4o'),
        use_vision=True,
    )
    result = await agent.run()
    print(result)  # Print output so FastAPI can capture it
    return result

if __name__ == "__main__":
    task_data = json.loads(sys.argv[1])  # Read task from FastAPI subprocess call
    asyncio.run(run_agent(task_data["task"]))
