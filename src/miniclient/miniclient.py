from tracim_daemon_sdk import TracimDaemonClient
from tracim_daemon_sdk.event import DAEMON_TRACIM_EVENT
from tracim_daemon_sdk.daemon_event import DaemonEvent
from tracim_daemon_sdk.data import TLMEvent
from tracim_daemon_sdk.helper import decode_json


def default_event_handler(c: TracimDaemonClient, e: DaemonEvent):
    tlm: TLMEvent = decode_json(e.data)
    print(tlm.event_type)


if __name__ == "__main__":
    client = TracimDaemonClient(
        master_socket_path='/home/mathieu/.config/TracimDaemon/master.sock',
        client_socket_path='/home/mathieu/PycharmProjects/TracimDaemonSDK_Python/tracim_daemon.sock',
    )
    client.create_client_socket()
    try:
        client.event_handlers[DAEMON_TRACIM_EVENT] = default_event_handler
        client.register_to_master()
        client.listen_to_events()
    finally:
        client.close()
