from pydantic import BaseModel, Field
from typing import List, Literal

class AnalysisOutput(BaseModel):
    intent: str = Field(description="The primary intent of the user's query.")
    complexity: Literal["Low", "Medium", "High"] = Field(description="The complexity of the query.")
    requires_tools: bool = Field(description="True if the query requires querying databases, semantic search, or web search to answer. False for general chat, greetings, or basic knowledge.")
    is_in_domain: bool = Field(description="True if the query is related to the business, company analytics, or professional domain. False if it is off-topic (e.g., cooking, unrelated hobbies).")

class PlanStep(BaseModel):
    tool: Literal["vector_tool", "web_tool", "sql_tool"] = Field(description="The tool to use for this step.")
    query: str = Field(description="The specific query or sub-task to pass to the tool.")
    source_type: Literal["INTERNAL_STRUCTURED", "INTERNAL_UNSTRUCTURED", "EXTERNAL_WEB", "MULTI_SOURCE"] = Field(description="The expected source of the information.")

class PlannerOutput(BaseModel):
    plan: List[PlanStep] = Field(description="The list of steps to execute in parallel.")
    requires_external_information: bool = Field(description="True if any sub-query requires searching the public web.")

class CheckerOutput(BaseModel):
    is_valid: bool = Field(description="Whether the draft answer is fully valid, complete, and grounded.")
    tool_selection_correct: bool = Field(description="If invalid, was the correct tool/information source used? (e.g. False if web_tool was needed but sql_tool was used).")
    missing_information: List[str] = Field(description="List of specific information that was missing from the evidence.")
    recommended_action: str = Field(description="Specific recommendation for the planner (e.g. 'Use web_tool to search for external inflation data'). Leave empty if valid.")
