from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from config.settings import (
    LLM_DEPLOYMENT_NAME,
    AZURE_BASE_URL,
    AZURE_API_KEY,
)

from prompts.agent_prompt import AGENT_SYSTEM_PROMPT

from tools.jira_tool import search_jira
from tools.confluence_tool import search_confluence
from tools.employee_tool import (
    get_employee,
    get_employee_leave_balance,
    get_employee_projects,
)
from tools.web_search_tool import search_web


# ============================================================
# LLM
# ============================================================

llm = ChatOpenAI(
    model=LLM_DEPLOYMENT_NAME,
    api_key=AZURE_API_KEY,
    base_url=AZURE_BASE_URL,
    temperature=0,
)


# ============================================================
# TOOLS
# ============================================================

TOOLS = [
    search_jira,
    search_confluence,
    search_web,
    get_employee,
    get_employee_leave_balance,
    get_employee_projects,
]


# ============================================================
# ROOT AGENT
# ============================================================

root_agent = create_agent(
    model=llm,
    tools=TOOLS,
    system_prompt=AGENT_SYSTEM_PROMPT,
)


def run_root_agent(
    user_question: str
):

    print("\n" + "=" * 70)
    print("🤖 ROOT AGENT")
    print("=" * 70)

    print(
        f"Question: {user_question}"
    )

    result = root_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_question,
                }
            ]
        }
    )

    return result
