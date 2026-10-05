# 🧠 Agentic RAG System

A highly autonomous, multi-agent Retrieval-Augmented Generation (RAG) system built with **LangGraph**, **Streamlit**, and **Ollama**. This system doesn't just retrieve documents—it analyzes intents, plans execution steps, routes traffic dynamically, writes and corrects its own SQL queries, and fuses information from multiple sources to provide grounded answers.

## ✨ Key Features

- **Multi-Agent Architecture**: Orchestrated via LangGraph (Analyzer, Planner, Executors, Reasoner, Checker).
- **Dynamic Routing**: Intelligently bypasses expensive database tools for simple queries (e.g., greetings) to provide instant responses.
- **Enterprise Guardrails**: Automatically detects and politely rejects off-topic or out-of-domain queries.
- **Self-Healing SQL Agent**: Queries structured data in CockroachDB. If a SQL query fails, the agent reads the database error and corrects its own code on the fly.
- **Multi-Source Fusion**: Seamlessly combines structured data (SQL), unstructured data (Pinecone Vector Search), and external data (Tavily Web Search).
- **100% Local Inference**: Powered by local `qwen2.5` via Ollama for privacy-first, offline AI execution.

## 🏗️ Architecture

1. **Analyzer**: Determines user intent, complexity, and domain relevance.
2. **Router & Guardrail**: Hijacks the workflow if the query is out-of-domain or doesn't require tools (Direct Response).
3. **Planner**: Breaks complex queries into parallel execution steps.
4. **Tools**:
   - `sql_tool`: LangChain SQL Agent connecting to CockroachDB.
   - `vector_tool`: Semantic search via Pinecone.
   - `web_tool`: Real-time web data via Tavily.
5. **Fusion & Reasoner**: Combines all evidence and generates a grounded draft answer without hallucinating.
6. **Checker**: Audits the draft. If evidence is missing, it routes back to the planner to try a different tool.

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.com/) (running locally)
- CockroachDB Cluster (or standard PostgreSQL)
- API Keys for Pinecone and Tavily

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/agentic-rag-system.git
   cd "Agentic RAG System"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Pull the Local LLM:**
   Make sure Ollama is running in the background, then pull the model:
   ```bash
   ollama pull qwen2.5
   ```

4. **Set up Environment Variables:**
   Create a `.env` file in the root directory and add your credentials:
   ```env
   PINECONE_API_KEY=your_pinecone_key
   TAVILY_API_KEY=your_tavily_key
   DATABASE_URL=cockroachdb://user:password@host:26257/defaultdb
   ```

### Running the Application

Start the Streamlit user interface:
```bash
streamlit run ui/streamlit_app.py
```

Open your browser to `http://localhost:8501`. 

*(To share with others on your local Wi-Fi, look for the Network URL in your terminal and ensure port `8501` is allowed through your Windows Firewall).*
