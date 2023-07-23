# TracimDaemonSDK

A python port for the TracimDaemonSDK, an SDK for the [TracimDaemon](https://github.com/Millefeuille42/TracimDaemon) project

## Usage

(WIP)

See source, below and [TracimDaemonSDK](https://github.com/Millefeuille42/TracimDaemonSDK) for usage.

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

