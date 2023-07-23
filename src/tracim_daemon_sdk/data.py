from typing import List, Any
from time import time

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    from argparse import Namespace


class TypeErrorData:
    def __init__(self, error: Exception):
        self.error: Exception = error


class TLMEvent:
    def __init__(self,
                 event_id: int = 0,
                 event_type: str = "",
                 read: Any = None,
                 created: time = None,
                 fields: Any = None):
        self.event_id: int = event_id
        self.event_type: str = event_type
        self.read: Any = read
        self.created: time = created
        self.fields: Any = fields


# Generic types

class DaemonClientData:
    def __init__(self, path: str, pid: str):
        self.path: str = path
        self.pid: str = pid


# Client to Daemon types

class DaemonClientAddData(DaemonClientData):
    pass


class DaemonClientDeleteData(DaemonClientData):
    pass


class DaemonDoRequestData:
    def __init__(self, method: str, endpoint: str, body: bytes):
        self.method: str = method
        self.endpoint: str = endpoint
        self.body: bytes = body


# Any to Any types

class DaemonAckData:
    def __init__(self, event_type: Any):
        self.type: Any = event_type


# Daemon to Client types

class DaemonRequestResultData:
    def __init__(self, request: DaemonDoRequestData, status_code: int, status: str, data: bytes):
        self.request: DaemonDoRequestData = request
        self.status_code: int = status_code
        self.status: str = status
        self.data: bytes = data


class DaemonAccountInfoData:
    def __init__(self, user_id: str):
        self.user_id: str = user_id


class DaemonClientsData(List[DaemonClientData]):
    pass


# Daemon to all Clients types

class DaemonTracimEventData:
    def __init__(self, tlm_event: TLMEvent):
        self.tlm_event: TLMEvent = tlm_event


class DaemonClientAddedData(DaemonClientData):
    pass


class DaemonClientDeletedData(DaemonClientData):
    pass
