"""
Shared settings for the Tor proxy (dperson/torproxy), employed by
commands/up (brings the container up) and commands/switch (changes identity
via the control port). The very same CONTROL_PASSWORD is used in both places.
"""

CONTAINER_NAME = "torproxy"
IMAGE = "dperson/torproxy"

HOST = "localhost"
PROXY_PORT = 9050
CONTROL_PORT = 9051
CONTROL_PASSWORD = "userbot-tor-control"
