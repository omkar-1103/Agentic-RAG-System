import os
import sys
from dotenv import load_dotenv
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.tools.sql_tool import execute_sql_agent
from app.tools.vector_tool import execute_vector_search

load_dotenv()

print("Testing Vector Tool...")
try:
    vector_res = execute_vector_search("company performance 2025")
    print(json.dumps(vector_res, indent=2))
except Exception as e:
    print("Vector Error:", e)

print("\nTesting SQL Tool...")
try:
    sql_res = execute_sql_agent("What was the company's performance in 2025?")
    print(json.dumps(sql_res, indent=2))
except Exception as e:
    print("SQL Error:", e)
