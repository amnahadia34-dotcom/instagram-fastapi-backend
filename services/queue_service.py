from collections import deque

event_queue = deque()

def push_event(event):
    event_queue.append(event)

def pop_event():
    if event_queue:
        return event_queue.popleft()
    return None
