import os
from langchain_community.utilities import SQLDatabase
from app.utils.logger import logger
from langchain_community.agent_toolkits import create_sql_agent
from langchain_ollama import ChatOllama

def execute_sql_agent(query: str) -> dict:
    """
    Executes a natural language query against CockroachDB by converting it to SQL.
    """
    logger.info(f"[SQL Tool] Querying CockroachDB for: {query}")
    
    db_uri = os.getenv("DATABASE_URL")
    if not db_uri or db_uri == "postgresql+psycopg2://user:password@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full":
        return {
            "source": "sql_tool",
            "query": query,
            "error": "DATABASE_URL is not configured properly."
        }
        
    try:
        # 1. Connect to CockroachDB
        db = SQLDatabase.from_uri(db_uri)
        
        # 2. Initialize the LLM for Text-to-SQL
        llm = ChatOllama(model="qwen2.5", temperature=0)
        
        # 3. Create the LangChain SQL Agent 
        # This agent automatically inspects the schema, writes SQL, runs it, and corrects errors
        agent_executor = create_sql_agent(llm, db=db, agent_type="tool-calling", verbose=True)
        
        # 4. Execute
        response = agent_executor.invoke({"input": query})
        
        return {
            "source": "sql_tool",
            "query": query,
            "results": response.get("output", "No results found.")
        }
    except Exception as e:
        return {
            "source": "sql_tool",
            "query": query,
            "error": str(e)
        }

