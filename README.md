<div align="center">
  <h1>🧠 Agentic RAG System</h1>
  <p><i>A highly autonomous, self-correcting Retrieval-Augmented Generation engine.</i></p>
  
  [![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
  [![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange.svg)](https://python.langchain.com/docs/langgraph/)
  [![Ollama](https://img.shields.io/badge/Ollama-100%25%20Local-white.svg)](https://ollama.com/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)](https://streamlit.io/)
</div>

---

## 🌟 Overview

The **Agentic RAG System** is not just another standard RAG pipeline that blindly fetches documents. It is a state-of-the-art **Multi-Agent System** that acts like a senior data analyst. 

When asked a question, it intelligently routes traffic, plans a multi-step execution strategy, writes and debugs its own SQL queries, searches the web for missing context, and strictly audits its own answers before showing them to the user.

---

## 🏗️ Full Pipeline Architecture

Below is the complete blueprint of how the LangGraph State Machine orchestrates the AI's thought process:

```mermaid
graph TD
    A([User Query]) --> B[🕵️ Analyzer]
    B --> C{🔀 Dynamic Router}
    
    %% Routes
    C -- "Out of Domain" --> D[🛡️ Guardrail]
    C -- "No Tools Needed" --> E[⚡ Direct Responder]
    C -- "Complex Query" --> F[📋 Planner]
    
    %% Execution
    F --> G1[(SQL / CockroachDB)]
    F --> G2[(Vector / Pinecone)]
    F --> G3[🌐 Web / Tavily]
    
    %% Synthesis
    G1 --> H[🔗 Fusion Node]
    G2 --> H
    G3 --> H
    
    H --> I[🧠 Reasoner]
    I --> J{✅ Checker / Auditor}
    
    %% Outcomes
    J -- "Valid & Grounded" --> K([Final Output])
    J -- "Missing Data / Error" --> F
    
    D --> K
    E --> K
    
    classDef default fill:#1E293B,stroke:#3B82F6,stroke-width:2px,color:#fff;
    classDef router fill:#3B82F6,stroke:#1D4ED8,color:#fff,stroke-width:2px;
    classDef tools fill:#0F766E,stroke:#0F766E,color:#fff,stroke-width:2px;
    
    class C,J router;
    class G1,G2,G3 tools;
```

### 🧠 Agent Explanations

1. **🕵️ Analyzer:** The entry point. It reads the query, determines the user's core intent, classifies the complexity, and decides if external tools are required.
2. **🔀 Router & 🛡️ Guardrail:** Evaluates the Analyzer's output. If a user asks about an unrelated topic (e.g., cooking recipes), the Guardrail rejects it politely. If it's a simple "Hello", it routes to the fast Direct Responder to save compute time.
3. **📋 Planner:** The system's architect. It breaks complex questions into a parallel execution plan, determining exactly which tools to query and how.
4. **🛠️ The Tools:**
   - **SQL Tool:** Uses LangChain's SQL Agent to query structured metrics from CockroachDB. It is capable of reading schema errors and rewriting its own broken SQL queries on the fly!
   - **Vector Tool:** Performs semantic search across unstructured data (PDFs/Docs) via Pinecone.
   - **Web Tool:** Searches the live internet via Tavily to answer questions about current events or external economic factors.
5. **🔗 Fusion Node:** Aggregates and standardizes the massive amounts of data returned from the parallel tool executions into a single context block.
6. **🧠 Reasoner:** Synthesizes the fused evidence to construct a comprehensive draft answer. It is strictly prompted *not* to hallucinate outside the provided evidence.
7. **✅ Checker (Self-Correction):** The QA Auditor. It grades the Reasoner's draft against the original query. If the answer is incomplete, or if the Planner used the wrong tool initially, it fails the check and loops the system backward to try again.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.com/) (running locally)
- CockroachDB Cluster
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
   Ensure Ollama is running, then pull the `qwen2.5` model (we recommend `qwen2.5:3b` or `1.5b` for faster local inference):
   ```bash
   ollama pull qwen2.5
   ```

4. **Set up Environment Variables:**
   Create a `.env` file in the root directory:
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

Navigate to `http://localhost:8501` in your browser to begin querying the system.

---
*Built with ❤️ utilizing LangGraph's multi-agent paradigm.*
