# services/queue_poll.py

"""
This module stores new Instagram comments in a simple
in-memory queue so Streamlit can poll them in real-time.
"""

comment_queue = []


def push_event(event: dict):
    """
    Webhook calls this to push a new comment into the queue.
    Example event:
    {
        "username": "...",
        "comment": "...",
        "comment_id": "..."
    }
    """
    comment_queue.append(event)


def get_event():
    """
    Streamlit calls this every 2 seconds to pull the next
    available comment event. If none, return None.
    """
    if len(comment_queue) == 0:
        return None

    return comment_queue.pop(0)
