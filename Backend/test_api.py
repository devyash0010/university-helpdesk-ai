"""
End-to-end API tests for the University Helpdesk Chatbot backend.

Usage:
    1. Start the backend:   uvicorn app:app --port 8010   (from Backend/)
    2. Run these tests:     python test_api.py

Set API_BASE to point at a different host/port (default http://127.0.0.1:8010).
"""

import asyncio
import io
import json
import os
import sys

import requests
import websockets

API_BASE = os.environ.get("API_BASE", "http://127.0.0.1:8010")
WS_URL = API_BASE.replace("http://", "ws://").replace("https://", "wss://") + "/ws/chat"

results = []


def check(name, passed, detail=""):
    results.append((name, bool(passed)))
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}" + (f" -- {detail}" if detail else ""))


def test_health():
    r = requests.get(f"{API_BASE}/", timeout=10)
    data = r.json()
    check(
        "GET / health check",
        r.status_code == 200 and data.get("status") == "running",
        json.dumps(data),
    )


def test_categories():
    r = requests.get(f"{API_BASE}/categories", timeout=10)
    data = r.json()
    ok = (
        r.status_code == 200
        and isinstance(data, list)
        and len(data) > 0
        and "category" in data[0]
        and isinstance(data[0].get("issues"), list)
        and len(data[0]["issues"]) > 0
    )
    check("GET /categories", ok, f"{len(data)} categories returned")
    return data


def test_chat(query="wifi is not working in my hostel"):
    r = requests.post(f"{API_BASE}/chat", json={"query": query}, timeout=120)
    data = r.json()
    suggestions = data.get("suggestions", [])
    ok = (
        data.get("success") is True
        and len(suggestions) == 3
        and all(
            {"issue", "category", "response"} <= set(s.keys())
            for s in suggestions
        )
    )
    check(
        "POST /chat semantic search",
        ok,
        f"top result: {suggestions[0]['issue'] if suggestions else 'none'}",
    )
    return suggestions


def test_issue_response(issue):
    r = requests.post(f"{API_BASE}/issue-response", json={"issue": issue}, timeout=120)
    data = r.json()
    ok = data.get("success") is True and bool(data.get("response"))
    check(
        "POST /issue-response",
        ok,
        str(data.get("response", ""))[:80],
    )


def test_create_ticket():
    payload = io.BytesIO(b"automated test attachment content")
    r = requests.post(
        f"{API_BASE}/create-ticket",
        data={"description": "Automated test ticket - please ignore"},
        files={"file": ("test_attachment.txt", payload, "text/plain")},
        timeout=30,
    )
    data = r.json()
    ticket = data.get("ticket") or {}
    ok = (
        data.get("success") is True
        and str(ticket.get("ticket_id", "")).startswith("TICK-")
        and ticket.get("status") == "open"
        and ticket.get("attachment") == "test_attachment.txt"
    )
    check("POST /create-ticket (with attachment)", ok, json.dumps(ticket))


def test_create_ticket_without_file():
    r = requests.post(
        f"{API_BASE}/create-ticket",
        data={"description": "No attachment test"},
        timeout=30,
    )
    data = r.json()
    ticket = data.get("ticket") or {}
    ok = (
        data.get("success") is True
        and str(ticket.get("ticket_id", "")).startswith("TICK-")
        and ticket.get("attachment") is None
    )
    check("POST /create-ticket (no attachment)", ok, json.dumps(ticket))


async def _websocket_exchange(query):
    async with websockets.connect(WS_URL, open_timeout=15) as ws:
        await ws.send(query)
        raw = await asyncio.wait_for(ws.recv(), timeout=120)
        return json.loads(raw)


def test_websocket():
    msg = asyncio.run(_websocket_exchange("my internet is very slow"))
    suggestions = msg.get("suggestions", [])
    ok = len(suggestions) == 3 and all(
        {"issue", "category", "response"} <= set(s.keys()) for s in suggestions
    )
    check(
        "WS /ws/chat real-time chat",
        ok,
        f"received {len(suggestions)} suggestions",
    )


def main():
    print(f"Running helpdesk API tests against {API_BASE}\n")
    test_health()
    test_categories()
    suggestions = test_chat()
    if suggestions:
        test_issue_response(suggestions[0]["issue"])
    test_create_ticket()
    test_create_ticket_without_file()
    test_websocket()

    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    print(f"\n{passed}/{total} tests passed")

    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    main()
