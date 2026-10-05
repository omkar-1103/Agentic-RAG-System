from langgraph.graph import StateGraph, END
from typing import Dict, Any
from app.utils.logger import logger

from app.state import GraphState
from app.config import config
from app.agents.analyzer import analyzer_node
from app.agents.planner import planner_node
from app.agents.fusion import fusion_node
from app.agents.reasoner import reasoner_node
from app.agents.checker import checker_node
from app.agents.direct_responder import direct_responder_node
from app.agents.guardrail import guardrail_node

# Import tools
from app.tools.vector_tool import execute_vector_search
from app.tools.web_tool import execute_web_search
from app.tools.sql_tool import execute_sql_agent

def execute_tools_node(state: GraphState) -> dict:
    """Reads the plan and executes tools in parallel."""
    logger.info("---EXECUTING TOOLS---")
    plan = state.get("plan", [])
    results = []
    
    for step in plan:
        tool_name = step.get("tool")
        query = step.get("query")
        
        if tool_name == "vector_tool":
            res = execute_vector_search(query)
            results.append(res)
        elif tool_name == "web_tool":
            res = execute_web_search(query)
            results.append(res)
        elif tool_name == "sql_tool":
            res = execute_sql_agent(query)
            results.append(res)
            
    return {"raw_evidence": results}

def analyzer_router(state: GraphState) -> str:
    """Routes based on whether tools are needed and if query is in domain."""
    if not state.get("is_in_domain", True):
        logger.info("---ROUTING TO GUARDRAIL (OUT OF DOMAIN)---")
        return "guardrail"
    elif state.get("requires_tools", True):
        logger.info("---ROUTING TO PLANNER (TOOLS REQUIRED)---")
        return "planner"
    else:
        logger.info("---ROUTING TO DIRECT RESPONDER (NO TOOLS NEEDED)---")
        return "direct_responder"

def checker_router(state: GraphState) -> str:
    """Routes based on Checker output."""
    is_valid = state.get("is_valid", False)
    retry_count = state.get("retry_count", 0)
    
    if is_valid:
        logger.info("---CHECK PASSED: END---")
        return "end"
    elif retry_count >= config.MAX_RETRIES:
        logger.info("---MAX RETRIES REACHED: END---")
        return "end"
    else:
        logger.info("---CHECK FAILED: ROUTING TO PLANNER---")
        return "planner"

# 1. Define the Graph
workflow = StateGraph(GraphState)

# 2. Add Nodes
workflow.add_node("analyzer", analyzer_node)
workflow.add_node("planner", planner_node)
workflow.add_node("executors", execute_tools_node)
workflow.add_node("fusion", fusion_node)
workflow.add_node("reasoner", reasoner_node)
workflow.add_node("checker", checker_node)
workflow.add_node("direct_responder", direct_responder_node)
workflow.add_node("guardrail", guardrail_node)

# 3. Add Edges
workflow.set_entry_point("analyzer")
workflow.add_conditional_edges(
    "analyzer",
    analyzer_router,
    {
        "guardrail": "guardrail",
        "planner": "planner",
        "direct_responder": "direct_responder"
    }
)
workflow.add_edge("direct_responder", END)
workflow.add_edge("guardrail", END)
workflow.add_edge("planner", "executors")
workflow.add_edge("executors", "fusion")
workflow.add_edge("fusion", "reasoner")
workflow.add_edge("reasoner", "checker")

# 4. Add Conditional Edge for Self-Correction
workflow.add_conditional_edges(
    "checker",
    checker_router,
    {
        "end": END,
        "planner": "planner"
    }
)

# 5. Compile
app = workflow.compile()
