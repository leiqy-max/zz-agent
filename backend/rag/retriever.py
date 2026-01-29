from sqlalchemy import text
from db import engine
from llm.embedding import embed_text

def retrieve_similar_documents(query: str, kb_type: str = "user", top_k: int = 3):
    query_embedding = embed_text(query)

    with engine.connect() as connection:
        # Construct SQL based on kb_type
        if kb_type == "all":
             sql = """
            SELECT id, content, metadata, embedding <-> (:query_embedding)::vector AS distance
            FROM documents
            ORDER BY distance ASC
            LIMIT :top_k;
            """
             params = {
                "query_embedding": query_embedding,
                "top_k": top_k
            }
        else:
             sql = """
            SELECT id, content, metadata, embedding <-> (:query_embedding)::vector AS distance
            FROM documents
            WHERE metadata->>'kb_type' = :kb_type OR metadata->>'kb_type' IS NULL
            ORDER BY distance ASC
            LIMIT :top_k;
            """
             params = {
                "query_embedding": query_embedding,
                "top_k": top_k,
                "kb_type": kb_type
            }

        # Use JSONB operator ->> to extract text value from metadata
        result = connection.execute(
            text(sql),
            params
        )

        return result.fetchall()
