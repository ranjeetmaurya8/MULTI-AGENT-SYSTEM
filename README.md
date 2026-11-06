# 🔍 AI-Powered Deep Research Chatbot

An AI-powered Deep Research Chatbot built using Python, LangChain, Groq, and Tavily. It uses specialized AI agents to search the web, gather relevant information, analyze research findings, and generate comprehensive research reports.

## 🚀 Live Demo

**Try the application:** https://multi-agent-system-cu57s4lktp7xunhncjg6xj.streamlit.app/

## ✨ Features

- 🔎 **Intelligent Web Search:** Search the web for relevant information using Tavily.
- 🤖 **Multi-Agent Architecture:** Uses specialized AI agents for research-related tasks.
- 📚 **Information Gathering:** Collects information from multiple web sources.
- 🧠 **Research Analysis:** Analyzes gathered information using LLMs.
- ✍️ **Report Generation:** Generates structured and informative research reports.
- 🌐 **Interactive UI:** User-friendly interface built with Streamlit.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| LangChain | Agent and LLM orchestration |
| Groq | LLM inference |
| GPT-OSS-20B | Language model |
| Tavily | Web search |
| Streamlit | Frontend and deployment |
| BeautifulSoup | Web scraping |
| Requests | HTTP requests |

## 📂 Project Structure

```text
MULTI-AGENT-SYSTEM/
│
├── app.py
├── agents.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/ranjeetmaurya8/MULTI-AGENT-SYSTEM.git
```

### 2. Navigate to the project folder

```bash
cd MULTI-AGENT-SYSTEM
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure API keys

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Never share or upload your API keys publicly.

### 7. Run the application

```bash
streamlit run app.py
```

## 🔑 API Requirements

- Groq API key
- Tavily API key

## 🌐 Deployment

The application is deployed using **Streamlit Community Cloud**.

**Live Application:** https://multi-agent-system-cu57s4lktp7xunhncjg6xj.streamlit.app/

## 👨‍💻 Author

**Ranjeet Maurya**

- GitHub: https://github.com/ranjeetmaurya8
- LinkedIn: https://linkedin.com/in/ranjeet-maurya-a23292318

---

⭐ If you find this project interesting, consider giving it a star!