# University Helpdesk Chatbot

A full-stack helpdesk chatbot designed to help students quickly find answers to university-related queries. It uses semantic search to find the best answers from a knowledge base. If the bot can't resolve the issue, the user can create a support ticket.

This is currently a Proof of Concept (POC) demonstrating how to combine **RAG-based retrieval, WebSockets, vector search, and a standard ticketing system**.

## Features

* **Real-time Chat:** WebSocket integration for seamless back-and-forth messaging.
* **Smart Search:** Uses LangChain and HuggingFace embeddings to understand the context of a student's question, rather than just matching keywords.
* **Vector Search:** Uses ChromaDB to store and retrieve semantically relevant knowledge-base entries.
* **Ticket Escalation:** If the knowledge base doesn't have a relevant answer, the user can create a support ticket, including file attachments.
* **Modular Setup:** Designed so the chat UI could eventually be embedded into an existing university website.

## Tech Stack

* **Frontend:** React.js, standard HTML/CSS, WebSocket Client
* **Backend:** Python, FastAPI, Uvicorn
* **AI & Search:** LangChain, HuggingFace (`all-MiniLM-L6-v2`), ChromaDB (Vector Database)
* **Data Processing:** Pandas, JSON

## How It Works

1. **Query:** A student asks a question via the React frontend.
2. **Search:** The FastAPI backend converts the query into an embedding and searches ChromaDB for similar issues in the university knowledge base.
3. **Response:** The most relevant solution is retrieved and sent back to the user.
4. **Fallback:** If the issue cannot be resolved, the student can create a support ticket for the admin/support team.
5. **Real-Time Communication:** WebSockets are used to provide real-time communication between the frontend and backend.

## Getting Started

### 1. Clone the repository

Bash

```bash
git clone https://github.com/YOUR_USERNAME/university-helpdesk-ai.git
cd university-helpdesk-ai
```

### 2. Backend Setup

Open a terminal and navigate to the backend folder:

Bash

```bash
cd backend
```

Create and activate a virtual environment:

Bash

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies and start the server:

Bash

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

*The API will run at* `http://localhost:8000`.
*You can view the API documentation at* `http://localhost:8000/docs`.

### 3. Frontend Setup

Open a new terminal window and navigate to the frontend folder:

Bash

```bash
cd frontend
```

Install the required packages and start the development server:

Bash

```bash
npm install
npm run dev
```

## Project Structure

Plaintext

```text
university-helpdesk-ai/
├── backend/
│   ├── app.py                 # FastAPI server and WebSocket routes
│   ├── requirements.txt
│   ├── data/
│   │   └── sample_query_categories.csv  # Sample knowledge base
│   └── uploads/               # Ticket attachments
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── README.md
└── .gitignore
```

*(Note: Production/university-specific data is intentionally excluded from this repository. A sanitized sample CSV is used for demonstration.)*

## Future Scope

* Build an embeddable widget version of the frontend.
* Add PostgreSQL for persistent ticket and user tracking.
* Implement student authentication and an admin dashboard.
* Add conversational memory (chat history).
* Add RAG evaluation and retrieval metrics.
* Support multiple universities with separate knowledge bases.
* Dockerize the application for easier deployment.
* Deploy the application to a cloud environment.

## Author

**Devyash Kulshrestha**

*B.Tech CSE (AI & Data Science)*
