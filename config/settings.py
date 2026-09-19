import os
from dotenv import load_dotenv

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}"
        )

    return value


# ============================================================
# Azure AI Foundry
# ============================================================

EMBEDDING_DEPLOYMENT_NAME = get_required_env(
    "EMBEDDING_DEPLOYMENT_NAME"
)

LLM_DEPLOYMENT_NAME = get_required_env(
    "LLM_DEPLOYMENT_NAME"
)

AZURE_BASE_URL = get_required_env(
    "AZURE_BASE_URL"
)

AZURE_API_KEY = get_required_env(
    "AZURE_API_KEY"
)


# ============================================================
# PostgreSQL
# ============================================================

DB_HOST = get_required_env("DB_HOST")
DB_PORT = get_required_env("DB_PORT")
DB_NAME = get_required_env("DB_NAME")
DB_USER = get_required_env("DB_USER")
DB_PASSWORD = get_required_env("DB_PASSWORD")


# ============================================================
# Atlassian
# ============================================================

ATLASSIAN_DOMAIN = get_required_env(
    "ATLASSIAN_DOMAIN"
)

ATLASSIAN_EMAIL = get_required_env(
    "ATLASSIAN_EMAIL"
)

ATLASSIAN_API_TOKEN = get_required_env(
    "ATLASSIAN_API_TOKEN"
)


# ============================================================
# Ngrok
# ============================================================

NGROK_AUTH_TOKEN = os.getenv(
    "NGROK_AUTH_TOKEN"
)
