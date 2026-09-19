# -*- coding: utf-8 -*-

import sys
import traceback

print("=" * 80, flush=True)
print("STEP 1: main.py STARTED", flush=True)
print("=" * 80, flush=True)

print(f"Python: {sys.version}", flush=True)
print(f"Executable: {sys.executable}", flush=True)
print(f"Working directory: {__import__('os').getcwd()}", flush=True)


# ============================================================
# IMPORT TESTS
# ============================================================

print("\nSTEP 2: Importing FastAPI...", flush=True)

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    print("✅ FastAPI import OK", flush=True)
except Exception:
    print("❌ FastAPI import FAILED", flush=True)
    traceback.print_exc()
    raise


print("\nSTEP 3: Importing uvicorn...", flush=True)

try:
    import uvicorn
    print("✅ Uvicorn import OK", flush=True)
except Exception:
    print("❌ Uvicorn import FAILED", flush=True)
    traceback.print_exc()
    raise


print("\nSTEP 4: Importing root agent...", flush=True)

try:
    from agent.root_agent import run_root_agent
    print("✅ Root agent import OK", flush=True)
except Exception:
    print("❌ Root agent import FAILED", flush=True)
    traceback.print_exc()
    raise


print("\nSTEP 5: Importing vector retriever...", flush=True)

try:
    from rag.vector_retriever import retrieve_vector_context
    print("✅ Vector retriever import OK", flush=True)
except Exception:
    print("❌ Vector retriever import FAILED", flush=True)
    traceback.print_exc()
    raise


print("\nSTEP 6: Importing configuration...", flush=True)

try:
    from config.settings import (
        LLM_DEPLOYMENT_NAME,
        AZURE_BASE_URL,
        AZURE_API_KEY,
    )

    print("✅ Config import OK", flush=True)

    print(
        f"LLM_DEPLOYMENT_NAME = {LLM_DEPLOYMENT_NAME}",
        flush=True
    )

    print(
        f"AZURE_BASE_URL = {AZURE_BASE_URL}",
        flush=True
    )

    print(
        f"AZURE_API_KEY loaded = {bool(AZURE_API_KEY)}",
        flush=True
    )

except Exception:
    print("❌ Config import FAILED", flush=True)
    traceback.print_exc()
    raise


print("\nSTEP 7: Importing system prompt...", flush=True)

try:
    from prompts.system_prompt import SYSTEM_PROMPT
    print("✅ System prompt import OK", flush=True)
except Exception:
    print("❌ System prompt import FAILED", flush=True)
    traceback.print_exc()
    raise


print("\nSTEP 8: Importing LangChain OpenAI...", flush=True)

try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import (
        SystemMessage,
        HumanMessage,
    )

    print("✅ LangChain OpenAI import OK", flush=True)

except Exception:
    print("❌ LangChain OpenAI import FAILED", flush=True)
    traceback.print_exc()
    raise


# ============================================================
# LLM
# ============================================================

print("\nSTEP 9: Creating LLM client...", flush=True)

try:

    llm = ChatOpenAI(
        model=LLM_DEPLOYMENT_NAME,
        api_key=AZURE_API_KEY,
        base_url=AZURE_BASE_URL,
        temperature=0,
    )

    print("✅ LLM client created", flush=True)

except Exception:
    print("❌ LLM client creation FAILED", flush=True)
    traceback.print_exc()
    raise


# ============================================================
# FASTAPI
# ============================================================

print("\nSTEP 10: Creating FastAPI application...", flush=True)

try:

    app = FastAPI(
        title="Enterprise Engineering Knowledge Copilot API"
    )

    print("✅ FastAPI application created", flush=True)

except Exception:
    print("❌ FastAPI application creation FAILED", flush=True)
    traceback.print_exc()
    raise


# ============================================================
# REQUEST MODEL
# ============================================================

class QueryRequest(BaseModel):
    question: str


print("\nSTEP 11: Registering routes...", flush=True)


@app.get("/")
def home():

    print("➡️ GET / called", flush=True)

    return {
        "status":
        "Enterprise Engineering Knowledge Copilot API is running!"
    }


@app.post("/query")
def run_copilot(req: QueryRequest):

    print("\n" + "=" * 80, flush=True)
    print("🚨 POST /query RECEIVED", flush=True)
    print("=" * 80, flush=True)

    try:

        user_question = req.question

        print(
            f"QUESTION: {user_question}",
            flush=True
        )

        # ----------------------------------------------------
        # ROOT AGENT
        # ----------------------------------------------------

        print(
            "\nSTEP A: Calling root agent...",
            flush=True
        )

        agent_result = run_root_agent(
            user_question
        )

        print(
            "✅ Root agent returned",
            flush=True
        )

        print(
            f"Agent result type: {type(agent_result)}",
            flush=True
        )

        print(
            f"Agent result keys: "
            f"{agent_result.keys() if isinstance(agent_result, dict) else 'N/A'}",
            flush=True
        )

        # ----------------------------------------------------
        # TOOL RESULTS
        # ----------------------------------------------------

        print(
            "\nSTEP B: Extracting tool results...",
            flush=True
        )

        messages = agent_result.get(
            "messages",
            []
        )

        print(
            f"Number of messages: {len(messages)}",
            flush=True
        )

        agent_context = []

        tool_was_used = False

        for index, message in enumerate(messages):

            print(
                f"\nMessage {index}",
                flush=True
            )

            print(
                f"Message type: "
                f"{getattr(message, 'type', None)}",
                flush=True
            )

            print(
                f"Message class: "
                f"{type(message)}",
                flush=True
            )

            if getattr(message, "type", None) == "tool":

                tool_was_used = True

                tool_name = getattr(
                    message,
                    "name",
                    "unknown"
                )

                print(
                    f"🔧 TOOL RESULT: {tool_name}",
                    flush=True
                )

                agent_context.append(
                    str(message.content)
                )

        combined_agent_context = "\n\n".join(
            agent_context
        )

        print(
            f"\nTools used: {tool_was_used}",
            flush=True
        )

        # ----------------------------------------------------
        # VECTOR SEARCH
        # ----------------------------------------------------

        print(
            "\nSTEP C: Calling pgvector...",
            flush=True
        )

        vector_results = retrieve_vector_context(
            user_question,
            limit=3
        )

        print(
            f"✅ Vector search returned "
            f"{len(vector_results)} results",
            flush=True
        )

        vector_context = []

        for index, item in enumerate(
            vector_results,
            start=1
        ):

            print(
                f"Vector result {index}: "
                f"{item.get('source_file')}",
                flush=True
            )

            vector_context.append(
                f"""
--- Vector Source {index} ---

File:
{item["source_file"]}

Type:
{item["source_type"]}

Distance:
{item["distance"]:.4f}

Content:
{item["content"]}
"""
            )

        combined_vector_context = "\n\n".join(
            vector_context
        )

        # ----------------------------------------------------
        # FINAL LLM
        # ----------------------------------------------------

        print(
            "\nSTEP D: Calling final LLM...",
            flush=True
        )

        final_prompt = f"""
User Question:

{user_question}

Information retrieved by the LangChain agent:

{combined_agent_context}

Information retrieved from PostgreSQL:

{combined_vector_context}

Return ONLY JSON:

{{
    "results": [],
    "citations": [],
    "confidence": "High|Medium|Low",
    "confidenceReason": [],
    "sources": []
}}
"""

        final_response = llm.invoke(
            [
                SystemMessage(
                    content=SYSTEM_PROMPT
                ),
                HumanMessage(
                    content=final_prompt
                ),
            ]
        )

        print(
            "✅ Final LLM returned",
            flush=True
        )

        final_text = final_response.content

        print(
            f"Final response type: {type(final_text)}",
            flush=True
        )

        print(
            f"Final response length: {len(str(final_text))}",
            flush=True
        )

        # ----------------------------------------------------
        # JSON
        # ----------------------------------------------------

        print(
            "\nSTEP E: Parsing final response...",
            flush=True
        )

        import json

        try:

            answer = json.loads(
                final_text
            )

            print(
                "✅ JSON parsing successful",
                flush=True
            )

        except Exception as exc:

            print(
                f"⚠️ JSON parsing failed: {exc}",
                flush=True
            )

            answer = {
                "results": [
                    final_text
                ],
                "citations": [],
                "confidence": "Low",
                "confidenceReason": [
                    "Final response was not valid JSON."
                ],
                "sources": [],
            }

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        print(
            "\nSTEP F: Returning API response...",
            flush=True
        )

        return {
            "question": user_question,
            "answer": answer,
            "data_source": (
                "hybrid_apis_and_vector_search"
                if tool_was_used or vector_results
                else "vector_search_only"
            )
        }

    except Exception as exc:

        print(
            "\n❌ ERROR INSIDE /query",
            flush=True
        )

        print(
            str(exc),
            flush=True
        )

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


print(
    "✅ STEP 11 COMPLETE - Routes registered",
    flush=True
)


# ============================================================
# SERVER
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 80, flush=True)
    print(
        "STEP 12: __name__ == '__main__'",
        flush=True
    )
    print("=" * 80, flush=True)

    print(
        "🚀 Starting Uvicorn...",
        flush=True
    )

    print(
        "📄 Swagger: http://127.0.0.1:8001/docs",
        flush=True
    )

    print(
        "🌐 Query: http://127.0.0.1:8001/query",
        flush=True
    )

    print(
        "❤️ Health: http://127.0.0.1:8001/",
        flush=True
    )

    try:

        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8001,
            reload=False,
            log_level="debug",
        )

    except Exception:

        print(
            "\n❌ UVICORN FAILED",
            flush=True
        )

        traceback.print_exc()

        raise

else:

    print(
        "\n⚠️ main.py was imported, "
        "not executed directly.",
        flush=True
    )
