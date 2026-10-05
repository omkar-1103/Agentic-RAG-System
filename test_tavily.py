import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.tools.web_tool import execute_web_search

load_dotenv()

import json
result = execute_web_search("What is the capital of France?")
print(json.dumps(result, indent=2))
