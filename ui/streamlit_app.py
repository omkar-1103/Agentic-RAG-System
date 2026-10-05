import sys
import os

# Add the parent directory to sys.path so it can import 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.graph import app as graph_app
from app.state import GraphState

# Ensure page config is first
st.set_page_config(page_title="Agentic RAG", page_icon="🤖", layout="wide")

# Custom CSS to make it even cleaner
st.markdown("""
<style>
    .chat-bubble { padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; }
    .agent-header { color: #2E86C1; font-weight: 600; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8616/8616088.png", width=60)
    st.title("Agentic RAG")
    st.markdown("This system uses multiple AI agents to break down your query, search SQL and Vector databases, and reason over the combined evidence.")
    st.divider()
    st.markdown("**Tools Available:**\n- 🗄️ CockroachDB (SQL)\n- 🌲 Pinecone (Vector)\n- 🌐 Web Search")

# Main Interface
st.title("🤖 Multi-Agent RAG System")
st.markdown("Ask complex questions. The agents will handle the rest.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("E.g., Compare the Q3 sales data with the latest strategy report..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Use st.status for a cleaner loading state
    with st.status("🧠 Agents are processing your query...", expanded=True) as status:
        st.write("Initializing Agentic Workflow...")
        
        # Initialize graph state
        initial_state = GraphState(
            original_query=prompt,
            intent="",
            complexity="",
            plan=[],
            raw_evidence=[],
            fused_evidence="",
            draft_answer="",
            checker_feedback="",
            is_valid=False,
            retry_count=0
        )
        
        try:
            current_state = initial_state.copy()
            # Run the graph and stream events
            for event in graph_app.stream(initial_state):
                for node_name, node_state in event.items():
                    current_state.update(node_state)
                    
                    if node_name == "analyzer":
                        st.markdown("### 1. 🕵️‍♂️ Query Analyzer")
                        st.info(f"**Intent Evaluated:** {node_state.get('intent', 'N/A')}\n\n**Complexity:** {node_state.get('complexity', 'N/A')}")
                        
                    elif node_name == "planner":
                        st.markdown("### 2. 📋 Planner")
                        plan = node_state.get("plan", [])
                        if plan:
                            for i, step in enumerate(plan):
                                st.write(f"**Step {i+1}:** Tool: `{step.get('tool')}` | Planned Query: `{step.get('query')}`")
                        else:
                            st.write("No specific tools planned.")
                            
                    elif node_name == "executors":
                        st.markdown("### 3. ⚡ Tool Execution")
                        evidence = node_state.get("raw_evidence", [])
                        for item in evidence:
                            st.write(f"**Tool:** `{item.get('source')}` | **Input:** `{item.get('query')}`")
                            with st.expander(f"View Output from {item.get('source')}"):
                                if "error" in item:
                                    st.error(item.get("error"))
                                else:
                                    st.write(item.get("results"))
                                    
                    elif node_name == "fusion":
                        pass # Fusion output will be displayed as input in reasoner step
                        
                    elif node_name == "reasoner":
                        st.markdown("### 4. 🧩 Reasoner")
                        with st.expander("View Reasoner Input (Fused Evidence)"):
                            st.write(current_state.get("fused_evidence", ""))
                        with st.expander("View Reasoner Output (Draft Answer)"):
                            st.write(node_state.get("draft_answer", ""))
                            
                    elif node_name == "checker":
                        st.markdown("### 5. ✅ Checker (Validation)")
                        with st.expander("View Checker Input"):
                            st.markdown("**Draft Answer being validated:**")
                            st.write(current_state.get("draft_answer", ""))
                        with st.expander("View Checker Output (Feedback)"):
                            st.write(f"**Is Valid:** `{node_state.get('is_valid')}`")
                            st.write(f"**Feedback:**\n{node_state.get('checker_feedback')}")

            status.update(label="✅ Workflow Complete!", state="complete", expanded=False)
            
            # Display assistant response
            answer = current_state.get("draft_answer", "Sorry, I couldn't generate an answer.")
            
            with st.chat_message("assistant"):
                st.markdown(f"### Final Answer\n{answer}")
                    
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            status.update(label="❌ Error occurred", state="error", expanded=True)
            st.error(f"An error occurred: {e}")
