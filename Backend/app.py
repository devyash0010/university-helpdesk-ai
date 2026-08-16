from fastapi import FastAPI, UploadFile, File, Form, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pandas as pd
import json
import os
import uuid

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


# ----------------------------------
# FastAPI Setup
# ----------------------------------

app = FastAPI(
    title="University Helpdesk Chatbot API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------
# Upload Folder
# ----------------------------------

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ----------------------------------
# Load CSV Knowledge Base
# ----------------------------------

df = pd.read_csv("alu_query_categories.csv")


# ----------------------------------
# Create LangChain Documents
# ----------------------------------

docs = []

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


# ----------------------------------
# Create Embeddings
# ----------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ----------------------------------
# Create Vector DB
# ----------------------------------

vector_db = Chroma.from_documents(docs, embeddings)


# ----------------------------------
# Request Models
# ----------------------------------

class Query(BaseModel):
    query: str


class Issue(BaseModel):
    issue: str


# ----------------------------------
# Health Check
# ----------------------------------

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Helpdesk chatbot backend running"
    }


# ----------------------------------
# Categories API
# ----------------------------------

@app.get("/categories")
def get_categories():

    data = []

    for _, row in df.iterrows():

        issues = json.loads(row["subcategories"])

        data.append({
            "category": row["label"],
            "issues": issues
        })

    return data


# ----------------------------------
# Chat API
# ----------------------------------

@app.post("/chat")
def chat(query: Query):

    try:

        results = vector_db.similarity_search(query.query, k=3)

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
            "error": str(e)
        }


# ----------------------------------
# Issue Response API
# ----------------------------------

@app.post("/issue-response")
def issue_response(issue: Issue):

    try:

        results = vector_db.similarity_search(issue.issue, k=1)

        if results:

            return {
                "success": True,
                "response": results[0].metadata["response"]
            }

        return {
            "success": False,
            "response": "Sorry, no solution found."
        }

    except Exception as e:

        return {
            "success": False,
            "response": str(e)
        }


# ----------------------------------
# Ticket Creation API
# ----------------------------------

@app.post("/create-ticket")
async def create_ticket(
    description: str = Form(...),
    file: UploadFile = File(None)
):

    try:

        file_name = None

        if file:

            file_name = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, file_name)

            with open(file_path, "wb") as f:
                f.write(await file.read())

        ticket = {
            "ticket_id": "TICK-" + str(uuid.uuid4())[:6],
            "status": "open",
            "description": description,
            "attachment": file_name
        }

        return {
            "success": True,
            "ticket": ticket
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# ----------------------------------
# WebSocket Chat
# ----------------------------------

@app.websocket("/ws/chat")
async def websocket_chat(ws: WebSocket):

    await ws.accept()

    try:

        while True:

            query = await ws.receive_text()

            results = vector_db.similarity_search(query, k=3)

            suggestions = []

            for r in results:

                suggestions.append({
                    "issue": r.metadata["issue"],
                    "category": r.metadata["category"],
                    "response": r.metadata["response"]
                })

            await ws.send_json({
                "suggestions": suggestions
            })

    except Exception:

        await ws.close()