from socket import socket, AF_UNIX, SOCK_STREAM
from typing import Any

from helper import encode_json


class DaemonEvent:
    def __init__(self, path: str = "", event_type: str = "", data: Any = None):
        self.path: str = path
        self.type: str = event_type
        self.data: Any = data


def send_daemon_event(event: DaemonEvent, target_socket: str):
    s = socket(AF_UNIX, SOCK_STREAM)
    s.connect(target_socket)
    try:
        s.send(encode_json(event).encode())
    finally:
        s.close()
