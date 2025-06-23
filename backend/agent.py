import datetime
from langchain.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from backend.memory import TaskMemory

llm = ChatOllama(model="mistral")
memory = TaskMemory()

planner_prompt = PromptTemplate.from_file("prompts/planner_prompt.txt", input_variables=["tasks", "history"])
planner_chain = LLMChain(llm=llm, prompt=planner_prompt)

def plan_day(today_tasks):
    history = memory.retrieve_recent(days=3)
    output = planner_chain.run({"tasks": today_tasks, "history": history})
    return output

def feedback_loop(tasks_done):
    memory.store_feedback(tasks_done)
    return "Feedback stored successfully."