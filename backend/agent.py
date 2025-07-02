import datetime
import os
import json
import asyncio
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from fpdf import FPDF

# Setup
ollama_host = os.getenv("OLLAMA_HOST", "localhost")
llm = ChatOllama(model="mistral", base_url=f"http://{ollama_host}:11434")
embeddings = OllamaEmbeddings(model="mistral")

# Persistent Chroma store
persist_directory = "data/chroma"
vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Prompts
planner_prompt = PromptTemplate.from_file("prompts/planner_prompt.txt", input_variables=["tasks", "history", "preferences"])
feedback_prompt = PromptTemplate.from_file("prompts/feedback_prompt.txt", input_variables=["feedback", "tasks"])
fine_tune_prompt = PromptTemplate.from_template("""
Based on the following historical performance data:

{history}

Update internal patterns to better plan for:
{tasks}

Return updated insight or strategy in one sentence.
""")

preferences_prompt = PromptTemplate.from_template("""
Update user preferences such as wake time, lunch time, dinner time, or task avoidance based on the feedback below.

Historical Context:
{history}

Recent Feedback:
{feedback}

Return updated user preferences in JSON format.
""")

weekly_review_prompt = PromptTemplate.from_template("""
You are a productivity analyst AI.

Here is a week's worth of feedback and daily plans:

{week_data}

Analyze patterns and suggest 3 personalized improvements for planning future weeks.

Keep it concise and actionable.
""")

# Chains
planner_chain = planner_prompt | llm | StrOutputParser()
feedback_chain = feedback_prompt | llm | StrOutputParser()
fine_tune_chain = fine_tune_prompt | llm | StrOutputParser()
preferences_chain = preferences_prompt | llm | StrOutputParser()
weekly_review_chain = weekly_review_prompt | llm | StrOutputParser()

PREFERENCE_FILE = "data/preferences.json"


def store_as_embedding(text, metadata):
    doc = Document(page_content=text, metadata=metadata)
    vectorstore.add_documents([doc])


def retrieve_history(query):
    results = retriever.invoke(query)
    return "\n".join([doc.page_content for doc in results])


def load_static_preferences():
    if os.path.exists(PREFERENCE_FILE):
        with open(PREFERENCE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_static_preferences(prefs):
    os.makedirs(os.path.dirname(PREFERENCE_FILE), exist_ok=True)
    with open(PREFERENCE_FILE, "w") as f:
        json.dump(prefs, f, indent=2)


def retrieve_preferences():
    return load_static_preferences()


def update_preferences_from_feedback(history, feedback):
    updated = preferences_chain.invoke({"history": history, "feedback": feedback})
    try:
        prefs = json.loads(updated)
        save_static_preferences(prefs)
        store_as_embedding(json.dumps(prefs, indent=2), {"type": "preferences", "timestamp": str(datetime.datetime.now())})
    except json.JSONDecodeError:
        pass


def plan_day(today_tasks):
    history = retrieve_history(today_tasks)
    preferences_dict = retrieve_preferences()
    preferences_json = json.dumps(preferences_dict, indent=2)
    output = planner_chain.invoke({
        "tasks": today_tasks,
        "history": history,
        "preferences": preferences_json
    })
    store_as_embedding(output, {"type": "plan", "timestamp": str(datetime.datetime.now())})
    return format_schedule(output)


def feedback_loop(tasks_done):
    history = retrieve_history(tasks_done)
    feedback_summary = feedback_chain.invoke({"feedback": tasks_done, "tasks": history})
    store_as_embedding(feedback_summary, {"type": "feedback", "timestamp": str(datetime.datetime.now())})

    reinforcement = fine_tune_chain.invoke({"history": history, "tasks": tasks_done})
    store_as_embedding(reinforcement, {"type": "insight", "timestamp": str(datetime.datetime.now())})

    update_preferences_from_feedback(history, tasks_done)
    return "Feedback stored and model updated with new insight."


def generate_weekly_review():
    docs = retriever.invoke("plan feedback insight")
    week_docs = []
    now = datetime.datetime.now()
    for doc in docs:
        ts = doc.metadata.get("timestamp")
        if ts:
            dt = datetime.datetime.fromisoformat(ts)
            if (now - dt).days <= 7:
                week_docs.append(doc.page_content)
    week_data = "\n".join(week_docs)
    review = weekly_review_chain.invoke({"week_data": week_data})
    store_as_embedding(review, {"type": "weekly_review", "timestamp": str(datetime.datetime.now())})
    return review


def export_to_pdf(title, content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line)
    filepath = f"data/exports/{filename}"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    pdf.output(filepath)
    return filepath


def get_memory_snapshot():
    results = retriever.invoke("plan feedback insight preferences")
    return [doc.page_content for doc in results if doc.metadata.get("type") in ["plan", "feedback", "insight", "preferences"]]


def format_schedule(text):
    lines = text.strip().split("\n")
    formatted = []
    for line in lines:
        if any(hour in line.lower() for hour in ["am", "pm"]):
            formatted.append(f"**{line.strip()}**")
        else:
            formatted.append(line.strip())
    return "\n\n".join(formatted)