import json
from app.state import GraphState
from app.utils.logger import logger

def fusion_node(state: GraphState) -> dict:
    """Fuses all raw evidence into a single context string."""
    logger.info("---FUSING EVIDENCE---")
    
    raw_evidence = state.get("raw_evidence", [])
    if not raw_evidence:
        return {"fused_evidence": "No evidence was retrieved."}
    
    # Format the evidence nicely for the Reasoner
    fused = "### RETRIEVED EVIDENCE ###\n\n"
    for item in raw_evidence:
        source = item.get("source", "unknown")
        query = item.get("query", "")
        fused += f"Source: {source} (Query: {query})\n"
        
        # Serialize the results depending on their format
        results = item.get("results")
        if isinstance(results, list):
            fused += "\n".join([f"- {str(r)}" for r in results])
        else:
            fused += str(results)
            
        fused += "\n\n"
        
    return {"fused_evidence": fused.strip()}
