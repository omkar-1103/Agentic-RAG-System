import os
from pinecone import Pinecone
from app.utils.logger import logger
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

def execute_vector_search(query: str) -> dict:
    """
    Executes a semantic search against a Pinecone Vector Database.
    """
    logger.info(f"[Vector Tool] Searching Pinecone for: {query}")
    
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME")
    
    if not api_key or not index_name:
        return {
            "source": "vector_tool",
            "query": query,
            "error": "Pinecone API key or Index Name is missing in .env."
        }
        
    try:
        # 1. Initialize Embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # 2. Connect to Pinecone Index
        pc = Pinecone(api_key=api_key)
        index = pc.Index(index_name)
        vectorstore = PineconeVectorStore(index=index, embedding=embeddings)
        
        # 3. Perform Similarity Search (Retrieve top 3 documents)
        docs = vectorstore.similarity_search(query, k=3)
        
        # 4. Format Results
        results = [doc.page_content for doc in docs]
        
        if not results:
            results = ["No relevant documents found in the vector database."]
            
        return {
            "source": "vector_tool",
            "query": query,
            "results": results
        }
        
    except Exception as e:
        return {
            "source": "vector_tool",
            "query": query,
            "error": str(e)
        }

