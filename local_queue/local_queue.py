from queue import Queue
from typing import Any, Callable


class MessageQueue:
    def __init__(self):
        self._queue = Queue()
        self._handlers = {}

    def add_message(self, message: Any):
        self._queue.put(message)

    def register_handler(self, message_type: type, handler: Callable):
        self._handlers[message_type] = handler

    def process_messages(self):
        while not self._queue.empty():
            message = self._queue.get()
            handler = self._handlers.get(type(message))
            if handler:
                handler(message)
            else:
                print(f"No handler registered for message type: {type(message).__name__}")
