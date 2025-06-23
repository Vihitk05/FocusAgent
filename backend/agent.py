import datetime
import os
from backend.memory import TaskMemory
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence


# llm = ChatOllama(model="mistral")
memory = TaskMemory()

ollama_host = os.getenv("OLLAMA_HOST", "localhost")
llm = ChatOllama(model="mistral", base_url=f"http://{ollama_host}:11434")

planner_prompt = PromptTemplate.from_file("prompts/planner_prompt.txt", input_variables=["tasks", "history"])
planner_chain = planner_prompt | llm  # This replaces LLMChain

def plan_day(today_tasks):
    history = memory.retrieve_recent(days=3)
    output = planner_chain.invoke({"tasks": today_tasks, "history": history})
    return output.content if hasattr(output, "content") else output

def feedback_loop(tasks_done):
    memory.store_feedback(tasks_done)
    return "Feedback stored successfully."