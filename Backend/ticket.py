import uuid
from datetime import datetime


def create_ticket(description, attachment=None):

    ticket = {
        "ticket_id": str(uuid.uuid4())[:8],
        "description": description,
        "attachment": attachment,
        "status": "open",
        "created_at": str(datetime.now())
    }

    return ticket