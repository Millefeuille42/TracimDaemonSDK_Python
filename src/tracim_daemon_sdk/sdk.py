from os import unlink, path, getpid
from socket import socket, AF_UNIX, SOCK_STREAM
from typing import Any

from helper import decode_json
from event import EVENT_TYPE_GENERIC, EVENT_TYPE_ERROR
from event import DAEMON_CLIENT_ADD, DAEMON_CLIENT_DELETE, DAEMON_TRACIM_EVENT, DAEMON_PONG, DAEMON_PING, DAEMON_ACCOUNT_INFO
from data import DaemonClientAddData, DaemonClientDeleteData, DaemonAccountInfoData, TypeErrorData, TLMEvent
from daemon_event import DaemonEvent, send_daemon_event


class TracimDaemonClient:
    def __init__(self, master_socket_path: str = "", client_socket_path: str = ""):
        self.client_socket_path: str = client_socket_path
        self.master_socket_path: str = master_socket_path
        self.event_handlers: dict[str, callable] = dict()
        self.user_id: int = 0
        self.client_socket: socket = socket(AF_UNIX, SOCK_STREAM)
        self.logger: callable = None
        self.event_handlers[DAEMON_PING] = default_ping_handler
        self.event_handlers[DAEMON_ACCOUNT_INFO] = default_account_info_handler
        self.event_handlers[EVENT_TYPE_ERROR] = default_account_info_handler

    def __del__(self):
        self.close()

    def __delete_client_socket(self):
        try:
            unlink(self.client_socket_path)
        except OSError:
            if path.exists(self.client_socket_path):
                raise

    def register_to_master(self):
        send_daemon_event(DaemonEvent(
            path=self.client_socket_path,
            event_type=DAEMON_CLIENT_ADD,
            data=DaemonClientAddData(
                path=self.client_socket_path,
                pid=str(getpid())
            )
        ), self.master_socket_path)

    def unregister_from_master(self):
        send_daemon_event(DaemonEvent(
            path=self.client_socket_path,
            event_type=DAEMON_CLIENT_DELETE,
            data=DaemonClientDeleteData(
                path=self.client_socket_path,
                pid=str(getpid())
            )
        ), self.master_socket_path)

    def close(self):
        self.unregister_from_master()
        self.__delete_client_socket()

    def create_client_socket(self):
        self.__delete_client_socket()
        self.client_socket.bind(self.client_socket_path)
        self.client_socket.listen(1)

    def log(self, message: Any):
        if self.logger is None:
            print(message)
        else:
            self.logger(message)

    def __call_handler(self, event_type: str, event: DaemonEvent):
        if event_type in self.event_handlers:
            self.event_handlers.get(event_type)(self, event)

    def listen_to_events(self):
        while 1:
            try:
                conn, _ = self.client_socket.accept()
            except KeyboardInterrupt:
                break
            try:
                while 1:
                    data: bytes = conn.recv(4096)
                    if not data:
                        break
                    event: DaemonEvent = decode_json(data)
                    self.__call_handler(EVENT_TYPE_GENERIC, event)
                    self.__call_handler(event.type, event)
                    if event.type == DAEMON_TRACIM_EVENT:
                        tlm_data: TLMEvent = decode_json(event.data)
                        self.__call_handler(tlm_data.event_type, event)
            except Exception as e:
                self.__call_handler(EVENT_TYPE_ERROR, DaemonEvent(
                    event_type=EVENT_TYPE_ERROR,
                    data=TypeErrorData(e)
                ))
            finally:
                conn.close()


def default_ping_handler(c: TracimDaemonClient, e: DaemonEvent):
    send_daemon_event(DaemonEvent(
        path=c.client_socket_path,
        event_type=DAEMON_PONG
    ), e.path)
    c.log(f"SOCKET: SEND: {DAEMON_PONG} -> {e.path}")


def default_account_info_handler(c: TracimDaemonClient, e: DaemonEvent):
    if e.path != c.master_socket_path:
        return
    data: DaemonAccountInfoData = decode_json(e.data)
    c.user_id = data.user_id
    c.log(f"SOCKET: RECV: {e.type} -> {e.path}")


def default_error_handler(c: TracimDaemonClient, e: DaemonEvent):
    error: TypeErrorData = decode_json(e.data)
    c.log(error.error)
