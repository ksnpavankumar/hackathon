Run the Agent + MCP + JSON Server + PostgreSQL
Assuming your project structure is:

Ragcodebase/
│
├── main.py
├── .env
├── requirements.txt
│
├── agent/
│   ├── __init__.py
│   └── root_agent.py
│
├── tools/
│   ├── __init__.py
│   ├── jira_tool.py
│   ├── confluence_tool.py
│   ├── web_tool.py
│   └── employee_mcp.py
│
├── prompts/
│   ├── __init__.py
│   └── agent_prompt.py
│
├── db.json
└── ...

1. Activate the Python environment
From Git Bash:

source .venv/Scripts/activate

You should see:

(.venv)

2. Start the Employee JSON Server
If your employee data is in db.json:

npx json-server --watch db.json --port 3000

Your employee API should then be available at:

http://localhost:3000

For example:

http://localhost:3000/employees

Keep this terminal running.

3. Start the Employee MCP server
Open a second terminal.

Activate the environment again:

source .venv/Scripts/activate

Then run your FastMCP server. For example, if your MCP file is:

tools/employee_mcp.py

run:

python tools/employee_mcp.py

Keep this terminal running as well.

If your MCP server uses a different filename, use that filename instead.

4. Start the main Agent
Open a third terminal.

source .venv/Scripts/activate

Then:

python main.py

You should see something similar to:

FastAPI + LangChain Enterprise Knowledge Copilot
Swagger Docs: http://127.0.0.1:8001/docs
Query Endpoint: http://127.0.0.1:8001/query

5. Your PostgreSQL database
Your PostgreSQL database is remote Azure PostgreSQL, so you do not need to start PostgreSQL locally.

Your .env should contain the connection information:

DB_HOST=...
DB_PORT=5432
DB_NAME=...
DB_USER=...
DB_PASSWORD=...

The agent connects to it when /query is called.

6. Overall startup
So locally you have three processes:

Terminal 1
   ↓
JSON Server
   ↓
localhost:3000
   ↓
Employee data


Terminal 2
   ↓
FastMCP Employee Server
   ↓
Employee tools


Terminal 3
   ↓
FastAPI + LangChain Root Agent
   ↓
localhost:8001
   ├── Employee MCP
   ├── Jira
   ├── Confluence
   ├── Web Search
   └── PostgreSQL + pgvector

7. Test the API
Open:

http://127.0.0.1:8001/docs

Use POST /query and try:

{
  "question": "Find the employee information for Alice Brown"
}

For a multi-tool test:

{
  "question": "Find Alice Brown's project assignments, check whether there are any related Jira tickets, search Confluence for documentation about the Core Banking Migration, and search the web for any recent security advisories relevant to the technologies she uses."
}

That should exercise the architecture where the root agent decides which tools are needed, rather than always calling every tool.