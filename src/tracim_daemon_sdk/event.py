# EVENT_TYPE_GENERIC is the event type for generic events (every DaemonEvent)
EVENT_TYPE_GENERIC = "custom_message"
# EVENT_TYPE_ERROR is the event type for errors
EVENT_TYPE_ERROR = "custom_error"

# ## Client to Daemon events ## #

DAEMON_CLIENT_ADD = "daemon_client_add"
DAEMON_CLIENT_DELETE = "daemon_client_delete"
DAEMON_GET_CLIENTS = "daemon_get_clients"
DAEMON_GET_ACCOUNT_INFO = "daemon_get_account_info"
DAEMON_DO_REQUEST = "daemon_do_request"

# ## Any to Any events ## #

DAEMON_ACK = "daemon_ack"
DAEMON_PING = "daemon_ping"
DAEMON_PONG = "daemon_pong"

# ## Daemon to Client events ## #

DAEMON_REQUEST_RESULT = "daemon_request_result"
DAEMON_ACCOUNT_INFO = "daemon_account_info"
DAEMON_CLIENTS = "daemon_clients"

# ## Daemon to all Clients events ## #

DAEMON_TRACIM_EVENT = "daemon_tracim_event"
DAEMON_CLIENT_ADDED = "daemon_client_added"
DAEMON_CLIENT_DELETED = "daemon_client_deleted"
