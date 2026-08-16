import pandas as pd
import json
import os

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


# -----------------------------
# Paths
# -----------------------------

BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "alu_query_categories.csv")
VECTOR_DB_PATH = os.path.join(BASE_DIR, "vector_db")


# -----------------------------
# Load CSV
# -----------------------------

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError("CSV file not found: alu_query_categories.csv")

df = pd.read_csv(CSV_PATH)

docs = []


# -----------------------------
# Convert CSV → Documents
# -----------------------------

for _, row in df.iterrows():

    issues = json.loads(row["subcategories"])
    templates = json.loads(row["templates"])

    for idx, issue in enumerate(issues):

        if idx < len(templates):
            response = templates[idx]["message"]
        else:
            response = templates[0]["message"]

        docs.append(
            Document(
                page_content=issue,
                metadata={
                    "category": row["label"],
                    "issue": issue,
                    "response": response
                }
            )
        )


# -----------------------------
# Embeddings Model
# -----------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -----------------------------
# Vector Database
# -----------------------------

if os.path.exists(VECTOR_DB_PATH):

    vector_db = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

else:

    vector_db = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=VECTOR_DB_PATH
    )

    vector_db.persist()


# -----------------------------
# Search Function
# -----------------------------

def search_query(query):

    try:

        if not query or query.strip() == "":
            return {
                "success": False,
                "suggestions": [],
                "error": "Empty query"
            }

        results = vector_db.similarity_search(query, k=3)

        suggestions = []

        for r in results:

            suggestions.append({
                "issue": r.metadata["issue"],
                "category": r.metadata["category"],
                "response": r.metadata["response"]
            })

        return {
            "success": True,
            "suggestions": suggestions
        }

    except Exception as e:

        return {
            "success": False,
            "suggestions": [],
            "error": str(e)
        }