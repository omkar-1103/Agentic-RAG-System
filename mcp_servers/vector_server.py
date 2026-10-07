import os
from mcp.server.fastmcp import FastMCP
from pinecone import Pinecone
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()

# Create the MCP Server
mcp = FastMCP("Pinecone Vector Search Server")


@mcp.tool()
def semantic_search(query: str, top_k: int = 3) -> str:
    """Search the Pinecone vector database for documents semantically similar to the query.
    Returns the top matching document contents.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
    vectorstore = PineconeVectorStore(index=index, embedding=embeddings)

    docs = vectorstore.similarity_search(query, k=top_k)
    results = [doc.page_content for doc in docs]
    return "\n---\n".join(results) if results else "No relevant documents found."


if __name__ == "__main__":
    mcp.run(transport="stdio")
