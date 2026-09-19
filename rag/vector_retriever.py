import os

import psycopg2

from dotenv import load_dotenv
from openai import OpenAI
from pgvector.psycopg2 import register_vector


load_dotenv()


# ============================================================
# CONFIG
# ============================================================

EMBEDDING_DEPLOYMENT_NAME = os.getenv(
    "EMBEDDING_DEPLOYMENT_NAME"
)

AZURE_BASE_URL = os.getenv(
    "AZURE_BASE_URL"
)

AZURE_API_KEY = os.getenv(
    "AZURE_API_KEY"
)

DB_HOST = os.getenv(
    "DB_HOST"
)

DB_PORT = os.getenv(
    "DB_PORT"
)

DB_NAME = os.getenv(
    "DB_NAME"
)

DB_USER = os.getenv(
    "DB_USER"
)

DB_PASSWORD = os.getenv(
    "DB_PASSWORD"
)


# ============================================================
# OPENAI CLIENT
# ============================================================

openai_client = OpenAI(
    api_key=AZURE_API_KEY,
    base_url=AZURE_BASE_URL,
)


# ============================================================
# VECTOR RETRIEVER
# ============================================================

def retrieve_vector_context(
    user_question: str,
    limit: int = 3,
):

    print(
        "\n🧠 Generating query embedding...",
        flush=True
    )

    response = openai_client.embeddings.create(
        input=[user_question],
        model=EMBEDDING_DEPLOYMENT_NAME,
        dimensions=1536,
    )

    embedding = response.data[0].embedding

    print(
        f"✅ Query embedding dimensions: {len(embedding)}",
        flush=True
    )

    if len(embedding) != 1536:

        raise RuntimeError(
            f"Expected 1536-dimensional embedding "
            f"but received {len(embedding)}"
        )

    # ========================================================
    # POSTGRESQL
    # ========================================================

    print(
        "🔌 Connecting to PostgreSQL...",
        flush=True
    )

    conn = None
    cursor = None

    try:

        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            sslmode="require",
        )

        register_vector(conn)

        print(
            "✅ PostgreSQL connection successful",
            flush=True
        )

        cursor = conn.cursor()

        # ====================================================
        # VERIFY DATABASE VECTOR DIMENSION
        # ====================================================

        cursor.execute(
            """
            SELECT vector_dims(content_vector)
            FROM enterprise_knowledge
            LIMIT 1;
            """
        )

        dimension_result = cursor.fetchone()

        if dimension_result:

            db_dimension = dimension_result[0]

            print(
                f"📐 PostgreSQL vector dimensions: "
                f"{db_dimension}",
                flush=True
            )

            if db_dimension != 1536:

                raise RuntimeError(
                    "Vector dimension mismatch: "
                    f"database={db_dimension}, "
                    f"query={len(embedding)}"
                )

        # ====================================================
        # VECTOR SEARCH
        # ====================================================

        print(
            "🔎 Running pgvector similarity search...",
            flush=True
        )

        vector_search_query = """
            SELECT
                source_file,
                source_type,
                linked_keys,
                content,
                (content_vector <=> %s::vector) AS distance
            FROM enterprise_knowledge
            ORDER BY content_vector <=> %s::vector
            LIMIT %s;
        """

        vector_str = str(embedding)

        cursor.execute(
            vector_search_query,
            (
                vector_str,
                vector_str,
                limit,
            )
        )

        rows = cursor.fetchall()

        print(
            f"✅ pgvector returned {len(rows)} results",
            flush=True
        )

        documents = []

        for row in rows:

            (
                source_file,
                source_type,
                linked_keys,
                content,
                distance,
            ) = row

            documents.append(
                {
                    "source_file": source_file,
                    "source_type": source_type,
                    "linked_keys": linked_keys,
                    "content": content,
                    "distance": float(distance),
                }
            )

        return documents

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

        print(
            "🔌 PostgreSQL connection closed",
            flush=True
        )
