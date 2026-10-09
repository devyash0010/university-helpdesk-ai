"""
Live demo script for University Helpdesk Chatbot.
Hits the running backend (default http://127.0.0.1:8010) and prints
a human-readable transcript. Also writes docs/DEMO.md for GitHub.

Usage (backend must be running):
    python scripts/demo.py
    python scripts/demo.py --base http://127.0.0.1:8010
"""
import argparse
import asyncio
import datetime
import io
import json
import os
import sys

import requests

try:
    import websockets
    HAS_WS = True
except ImportError:
    HAS_WS = False


def section(title):
    bar = "=" * 60
    return f"\n{bar}\n{title}\n{bar}\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=os.environ.get("API_BASE", "http://127.0.0.1:8010"))
    parser.add_argument("--query", default="wifi not working in hostel")
    parser.add_argument("--out", default="docs/DEMO.md")
    args = parser.parse_args()
    base = args.base.rstrip("/")

    lines = []
    lines.append("# University Helpdesk Chatbot — Live Demo")
    lines.append("")
    lines.append(f"_Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} against `{base}`_")
    lines.append("")

    print(section(f"1) Health check  GET {base}/"))
    r = requests.get(f"{base}/", timeout=10)
    print(r.status_code, r.text)
    lines.append("## 1. Health check `GET /`")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(r.json(), indent=2))
    lines.append("```")
    lines.append("")

    print(section(f"2) Categories  GET {base}/categories"))
    r = requests.get(f"{base}/categories", timeout=10)
    cats = r.json()
    print(f"Got {len(cats)} categories, first: {cats[0]}")
    lines.append("## 2. Categories `GET /categories`")
    lines.append("")
    lines.append(f"Backend returns **{len(cats)} categories**. Example:")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(cats[:2], indent=2))
    lines.append("```")
    lines.append("")

    print(section(f"3) Semantic chat  POST {base}/chat  query={args.query!r}"))
    r = requests.post(f"{base}/chat", json={"query": args.query}, timeout=120)
    data = r.json()
    suggestions = data.get("suggestions", [])
    for s in suggestions:
        print(f" - {s['issue']} [{s['category']}] -> {s['response'][:90]}")
    lines.append(f"## 3. Semantic chat `POST /chat` — query: \"{args.query}\"")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(data, indent=2)[:3000])
    lines.append("```")
    lines.append("")

    if suggestions:
        top = suggestions[0]["issue"]
        print(section(f"4) Issue response  POST {base}/issue-response  issue={top!r}"))
        r = requests.post(f"{base}/issue-response", json={"issue": top}, timeout=120)
        print(r.text[:500])
        lines.append(f"## 4. Issue response `POST /issue-response` — issue: \"{top}\"")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(r.json(), indent=2))
        lines.append("```")
        lines.append("")

    print(section(f"5) Ticket creation  POST {base}/create-ticket"))
    payload = io.BytesIO(b"demo attachment from demo script")
    r = requests.post(
        f"{base}/create-ticket",
        data={"description": "Demo ticket: wifi issue in hostel, please help"},
        files={"file": ("demo_note.txt", payload, "text/plain")},
        timeout=30,
    )
    print(r.text)
    lines.append("## 5. Ticket creation `POST /create-ticket`")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(r.json(), indent=2))
    lines.append("```")
    lines.append("")

    if HAS_WS:
        print(section("6) WebSocket real-time chat  /ws/chat"))

        async def ws_demo():
            ws_url = base.replace("http://", "ws://").replace("https://", "wss://") + "/ws/chat"
            async with websockets.connect(ws_url, open_timeout=15) as ws:
                await ws.send("my internet is very slow")
                raw = await asyncio.wait_for(ws.recv(), timeout=120)
                return json.loads(raw)

        try:
            msg = asyncio.run(ws_demo())
            print(f"WS returned {len(msg.get('suggestions', []))} suggestions")
            lines.append("## 6. WebSocket real-time chat `/ws/chat`")
            lines.append("")
            lines.append("Send `\"my internet is very slow\"` → receive 3 suggestions:")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(msg, indent=2)[:2500])
            lines.append("```")
            lines.append("")
        except Exception as e:
            print(f"WS demo failed: {e}")
            lines.append(f"WebSocket demo failed: {e}\n")

    lines.append("---")
    lines.append("Run it yourself: `python scripts/demo.py` with the backend running "
                 "(`uvicorn main:app --host 127.0.0.1 --port 8010` from `Backend/`).")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    sys.exit(main())
