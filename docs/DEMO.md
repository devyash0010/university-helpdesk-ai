# University Helpdesk Chatbot — Live Demo

_Generated: 2026-10-09 09:56:40 against `http://127.0.0.1:8010`_

## 1. Health check `GET /`

```json
{
  "status": "running",
  "service": "University Helpdesk Chatbot Backend"
}
```

## 2. Categories `GET /categories`

Backend returns **7 categories**. Example:

```json
[
  {
    "category": "Login & Access Issues",
    "issues": [
      "Username not found",
      "Forgot password / Reset password",
      "Session timeout"
    ]
  },
  {
    "category": "Registration Form Issues",
    "issues": [
      "Unable to download submitted form",
      "Payment status not updated",
      "Registration form not opening",
      "Registration form not submitting",
      "Error: No User Found"
    ]
  }
]
```

## 3. Semantic chat `POST /chat` — query: "wifi not working in hostel"

```json
{
  "success": true,
  "suggestions": [
    {
      "issue": "Exam centre unreachable",
      "category": "Emergency / Time-Sensitive Issues",
      "response": "Admit card has been released on emergency basis. Download immediately from portal."
    },
    {
      "issue": "Registration form not opening",
      "category": "Registration Form Issues",
      "response": "save"
    },
    {
      "issue": "Error: No User Found",
      "category": "Registration Form Issues",
      "response": "Registration form issue resolved. Clear cache (Ctrl+Shift+Delete) and try again."
    }
  ]
}
```

## 4. Issue response `POST /issue-response` — issue: "Exam centre unreachable"

```json
{
  "success": true,
  "response": "Admit card has been released on emergency basis. Download immediately from portal."
}
```

## 5. Ticket creation `POST /create-ticket`

```json
{
  "success": true,
  "ticket": {
    "ticket_id": "TICK-544249",
    "status": "open",
    "description": "Demo ticket: wifi issue in hostel, please help",
    "attachment": "demo_note.txt"
  }
}
```

## 6. WebSocket real-time chat `/ws/chat`

Send `"my internet is very slow"` → receive 3 suggestions:

```json
{
  "success": true,
  "suggestions": [
    {
      "issue": "Unable to download submitted form",
      "category": "Registration Form Issues",
      "response": "Registration form issue resolved. Clear cache (Ctrl+Shift+Delete) and try again."
    },
    {
      "issue": "Payment issues",
      "category": "Form Related Issues",
      "response": "Your query has been resolved. Please check . If you still face any issue, feel free to contact us."
    },
    {
      "issue": "Old data not fetched",
      "category": "Form Related Issues",
      "response": "Your query has been resolved (Subject change). Please check . If you still face any issue, feel free to contact us."
    }
  ]
}
```

---
Run it yourself: `python scripts/demo.py` with the backend running (`uvicorn main:app --host 127.0.0.1 --port 8010` from `Backend/`).