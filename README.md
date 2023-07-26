# TracimDaemonSDK

A python port for the TracimDaemonSDK, an SDK for the [TracimDaemon](https://github.com/Millefeuille42/TracimDaemon) project

For a quickstart see [TracimDaemon Quickstart](https://github.com/Millefeuille42/TracimDaemon_QuickStart)

## Usage

Get the package

```bash
pip install tracim_daemon_sdk
```

Create a new TracimDaemon client

```python
from tracim_daemon_sdk import TracimDaemonClient

if __name__ == "__main__":
    client = TracimDaemonClient(
        master_socket_path='/home/user/.config/TracimDaemon/master.sock',
        client_socket_path='/home/user/.config/MiniClient/socket.sock',
    )
```

Create and listen to the client socket

```python
from tracim_daemon_sdk import TracimDaemonClient

if __name__ == "__main__":
    client = TracimDaemonClient(
        master_socket_path='/home/mathieu/.config/TracimDaemon/master.sock',
        client_socket_path='/home/mathieu/PycharmProjects/TracimDaemonSDK_Python/tracim_daemon.sock',
    )
    client.create_client_socket()
```

From now on it is recommended to wrap the rest of the code in a try/finally block to ensure the socket is closed properly

```python
from tracim_daemon_sdk import TracimDaemonClient

if __name__ == "__main__":
    client = TracimDaemonClient(
        master_socket_path='/home/mathieu/.config/TracimDaemon/master.sock',
        client_socket_path='/home/mathieu/PycharmProjects/TracimDaemonSDK_Python/tracim_daemon.sock',
    )
    client.create_client_socket()
    try:
        pass
    finally:
        client.close()
```

Set up various handlers then register the client to the daemon and start listening to events

```python
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
```

The "minimal" client code is as above.

## Handlers and data

A handler follows the `EventHandler` definition (see below).
If the event type is expecting data, it is possible to parse it using the helper functions

```python
from tracim_daemon_sdk import TracimDaemonClient
from tracim_daemon_sdk.daemon_event import DaemonEvent
from tracim_daemon_sdk.data import TLMEvent
from tracim_daemon_sdk.helper import decode_json

def default_event_handler(c: TracimDaemonClient, e: DaemonEvent):
    tlm: TLMEvent = decode_json(e.data)
    print(tlm.event_type)

```

This handler stores the parsed data in a `TLMEvent` object and prints the event type.

## Definitions

### TLMEvent

TLMEvent is the class that represents the data sent by Tracim (see tracim TLM documentation)

```python
from time import time
from typing import Any

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
```

### DaemonEvent

DaemonEvent is the event format used to communicate between apps

```python
from typing import Any

class DaemonEvent:
    def __init__(self, path: str = "", event_type: str = "", data: Any = None):
        self.path: str = path
        self.type: str = event_type
        self.data: Any = data
```

- The `path` field is the path to the client socket (as defined in the config)
- The `type` field is any of the constants defined in event.py
- The `data` field can contain additional information of any format

A `type` is expected to contain additional data if there is a `<eventType>Data` class defined in `data.py`.

### EventHandler

EventHandler is the function definition for the event handlers.
It takes a `TracimDaemonClient` and a `DaemonEvent` as parameters

```python
from tracim_daemon_sdk import TracimDaemonClient
from tracim_daemon_sdk.daemon_event import DaemonEvent

def handler(c: TracimDaemonClient, e: DaemonEvent) -> None:
    pass
```

By default, handlers for `DAEMON_ACCOUNT_INFO` and `DAEMON_PING` are already defined, it is possible to override them.

### Event types

Event types are defined by tracim. It is also possible to set handlers for every `DaemonEvent` type.
There also is events defined by the SDK, for convenience.

```go
# EVENT_TYPE_GENERIC is the event type for generic events (every DaemonEvent)
EVENT_TYPE_GENERIC = "custom_message"
# EVENT_TYPE_ERROR is the event type for errors
EVENT_TYPE_ERROR = "custom_error"
```

## Protocol (for developers of another language)

### Communication

Client and daemons communicate with the `DaemonEvent` format, i.e. JSON data following this format:

```json
{
    "type": "event_type",
    "path": "/path/to/client/socket",
    "data": {}
}
```

(See above `DaemonEvent` section for details about each field)

### Registering / unregistering a client

When registering / unregistering a client a `DaemonEvent` must be sent on the daemon socket.

```json
{
    "type": "client_add",
    "path": "/path/to/client/socket",
    "data": {
      "path": "/path/to/client/socket",
      "pid": "999"
    }
}
```

To register a client, the client must send the message to the daemon socket, with the `type` field set to `client_add`.
To unregister a client, the client must send the message to the daemon socket, with the `type` field set to `client_delete`.

In both, additional info, defined as follows, is required:

```json
{
  "path": "/path/to/client/socket",
  "pid": "999"
}
```

With `pid` being the PID of the client process.

### Receiving events

Once registered, the client will receive `DaemonEvent`s from the daemon.

(See above `DaemonEvent` section for details about types and data)

### Ack and Keep-Alive

#### Ack

The daemon will send a `DaemonAck` upon receiving any managed events not expecting a response, otherwise the 
expected response is sent. As for now, a `DaemonPong` for a `DaemonPing` and a `DaemonAccountInfo` for a `DaemonClientAdd`

The daemon expects no `DaemonAck` on its messages.

#### Keep-Alive

The daemon will periodically (once every minute) send a `DaemonPing` event, clients have a minute to respond with `DaemonPong`,
If not, it will unregister un-responding clients at the next ping.

It is possible to test the daemon responsiveness by sending it `DaemonPing` events. It will respond with a `DaemonPong` as soon as possible.

