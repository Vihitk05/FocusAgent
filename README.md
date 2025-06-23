# 🧠 FocusAgent — A Self-Learning AI Task Planner

FocusAgent is an offline, privacy-first AI agent that learns how you work and helps you plan your day better — one task at a time. No black-box APIs. No cloud dependency. Just open-source LLMs, memory, and a feedback loop.

Built with:
- 🧱 LangChain + Ollama (`mistral` by default)
- 🧠 ChromaDB-style memory (simple JSON log)
- 🖥️ Streamlit frontend
- 🐍 Python backend

---

## 📦 Features

- ✍️ Input tasks → get a personalized day plan
- 🔁 Give daily feedback → the agent adapts weekly
- 💾 Full local memory using structured logs
- 🧠 Uses Mixtral/Mistral via Ollama for planning and reasoning
- 🔒 100% offline: No API keys, no telemetry

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git https://github.com/Vihitk05/FocusAgent.git
cd FocusAgent
```

### 2. Install Ollama

If you're on macOS (M1/M2):
```bash
brew install ollama
```

Pull the model:
```bash
ollama pull mistral
```

Keep it running:
```bash
ollama run mistral
```

---

### 3. Set Up Python Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 4. Run the App

From the project root:

```bash
streamlit run frontend/app.py
```

---

## 📁 Project Structure

```
focusagent/
├── backend/
│   ├── agent.py         # LLM + planning logic
│   └── memory.py        # Task memory and feedback log
├── frontend/
│   └── app.py           # Streamlit UI
├── data/
│   └── logs.json        # Persistent memory store
├── prompts/
│   └── planner_prompt.txt  # Daily planner LLM prompt
└── requirements.txt
```

---

## 🧠 How It Works

1. **You enter tasks** in the web UI
2. The agent pulls recent behavior from `logs.json`
3. It generates a suggested schedule using `mistral`
4. **You give feedback** at the end of the day
5. The agent stores your feedback and adjusts future plans

---

## 🧪 Example Use

```
Input:
- Finish LLM blog post
- Reply to emails
- Prep for design review

Agent Suggests:
- 9AM–11AM: Blog writing (deep work)
- 11AM–12PM: Emails (light)
- 2PM–3PM: Design prep
```

## 🐳 Docker Deployment

### 1. Start Ollama (if not already running)
Make sure Ollama is running on your host machine:
```bash
ollama serve
```
If you see `bind: address already in use`, Ollama is already running. You can check this using:
```bash
lsof -i :11434
```

### 2. Build the Docker Image
```bash
docker build -t focusagent .
```

### 3. Run the Container
```bash
docker run -p 8501:8501 \
  -e OLLAMA_HOST=host.docker.internal \
  -v "$(pwd)/data":/app/data \
  focusagent
```
> `host.docker.internal` lets the container access the Ollama server on your Mac host.

### 4. Open in Browser
Go to: [http://localhost:8501](http://localhost:8501)

✅ The container will persist feedback data using the shared `./data` volume.

---

## 🚧 Roadmap

- [ ] Emotion tagging for better prioritization
- [ ] Calendar sync support
- [ ] Contextual file inspection

---

## 🔓 License

MIT — open to use, improve, fork, remix.

---

## 👋 Contribute or Extend?

Want to add GPT-4 support, mobile view, or calendar sync? Open an issue or PR — let’s build smarter tools together.
