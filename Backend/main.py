from fastapi import FastAPI, WebSocket, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pandas as pd
import json
import os

from chatbot import search_query


# -------------------------------
# FastAPI App
# -------------------------------

app = FastAPI(
    title="University Helpdesk Chatbot API",
    version="1.0"
)


# -------------------------------
# Enable CORS
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# Upload Folder
# -------------------------------

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# -------------------------------
# Load CSV Knowledge Base
# -------------------------------

df = pd.read_csv("alu_query_categories.csv")


# -------------------------------
# Request Models
# -------------------------------

class ChatRequest(BaseModel):
    query: str


class IssueRequest(BaseModel):
    issue: str


# -------------------------------
# Health Check
# -------------------------------

@app.get("/")
def home():

    return {
        "status": "running",
        "service": "University Helpdesk Chatbot Backend"
    }


# -------------------------------
# Categories API (Quick Help)
# -------------------------------

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


# -------------------------------
# Chat API
# -------------------------------

@app.post("/chat")
def chat(req: ChatRequest):

    try:

        result = search_query(req.query)

        return result

    except Exception as e:

        return {
            "success": False,
            "suggestions": [],
            "error": str(e)
        }


# -------------------------------
# Issue Response API
# -------------------------------

@app.post("/issue-response")
def issue_response(req: IssueRequest):

    try:

        result = search_query(req.issue)

        if result["suggestions"]:

            return {
                "success": True,
                "response": result["suggestions"][0]["response"]
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


# -------------------------------
# Ticket API
# -------------------------------

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
            "ticket_id": "TICK1021",
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


# -------------------------------
# WebSocket Chat
# -------------------------------

@app.websocket("/ws/chat")
async def websocket_chat(ws: WebSocket):

    await ws.accept()

    try:

        while True:

            query = await ws.receive_text()

            result = search_query(query)

            await ws.send_json(result)

    except Exception:

        await ws.close()