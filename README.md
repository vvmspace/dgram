# DGram

**Command your own Telegram accounts from the terminal — securely, elegantly, and without a single re-login.**

DGram is a compact Python toolkit that turns a Telegram Desktop `tdata` folder into a fully-fledged, scriptable Telegram session. No QR codes, no verification codes, no fumbling about with API credentials by hand: point a command at your `tdata` folder and it converts, authenticates, and connects — every single time, routed through Tor for good measure.

Whether you are orchestrating a personal userbot, wiring up bespoke Telegram automation, or simply prefer a keyboard to a touchscreen, DGram gives you a tidy set of shell-ready commands for reading messages, sending them, and managing groups — all built atop [Telethon](https://github.com/LonamiWebs/Telethon) and [opentele](https://github.com/thedemons/opentele).

## Why DGram

- **Zero re-authentication.** Reuses your existing Telegram Desktop session (`tdata`) directly — the account stays logged in, exactly as you left it.
- **Private by design.** Every connection — to Telegram, and nowhere else — is routed through a local Tor SOCKS5 proxy, courtesy of [`dperson/torproxy`](https://hub.docker.com/r/dperson/torproxy) in Docker.
- **One command, one job.** Each utility does a single thing well: no bloated multi-purpose binary, no configuration files to wrangle.
- **Delightfully easy to extend.** Every command is a self-contained, shebanged Python script of well under a hundred lines, built on one shared client factory (`libs/dgram.get_client`). Adding a new capability is a matter of minutes, not an afternoon.
- **Genuinely portable.** No installation, no daemons, no background services beyond the proxy itself. Run a command; it does its work and exits.

## Requirements

- Python 3.12 or newer, managed via [`uv`](https://docs.astral.sh/uv/)
- Docker, for the bundled Tor proxy
- A `tdata` folder from an existing Telegram Desktop installation

## Quickstart

Bring the Tor proxy up, then talk to Telegram through it:

```sh
commands/up                                   # starts the torproxy container
commands/conversations path/to/tdata          # lists every dialogue, group and channel
commands/messages path/to/tdata -l 10          # prints the ten most recent messages
commands/send_message path/to/tdata @friend "Good evening!"
commands/down                                 # stops the proxy once you are done
```

Every command follows the very same shape: `commands/<name> path/to/tdata [arguments…]`. No installation step, no virtual environment to activate by hand — `uv` handles all of that via the shebang line at the top of each script.

## Command reference

| Command | Purpose |
|---|---|
| `up` | Brings up (or recreates) the Tor proxy container, publishing the SOCKS5 and control ports |
| `down` | Stops the Tor proxy container, keeping its data volumes intact |
| `switch [-h host] [-p port] [-c control-port]` | Requests a fresh Tor identity and confirms the exit IP address changed |
| `conversations path/to/tdata` | Lists dialogues, groups and channels |
| `messages path/to/tdata [-l length] [-c conversation_id] [-s ASC\|DESC]` | Prints recent messages, including your own, from one dialogue or across the lot |
| `send_message path/to/tdata target "text"` | Sends a message; joins the target group first if you are not yet a member |
| `wait path/to/tdata PATTERN [-t timeout] [-c conversation_id] [-m message]` | Waits for an incoming message matching a pattern, optionally sending one first |
| `join path/to/tdata @group` | Joins a group, channel or invite link |
| `leave path/to/tdata @group` | Leaves a group or channel |
| `group_create path/to/tdata "Title" @username` | Creates a new public supergroup |
| `group_invite path/to/tdata @user @group` | Invites a user into a group |
| `group_delete path/to/tdata @group` | Deletes a group |
| `search_groups path/to/tdata "query"` | Searches Telegram's own directory for public groups |

Run any command with `-h`/`--help` for its full argument list.

## Architecture, in brief

```
libs/dgram.py   -> get_client(tdata_path)   converts tdata to an authenticated TelegramClient, over Tor
libs/tor.py     -> shared Tor proxy/container settings, used by up, down and switch
commands/*      -> one shebanged script per capability, each a thin, readable wrapper around libs/dgram
```

Every command is under a hundred lines and reads top to bottom without surprises: parse arguments, obtain a client, do the one thing the command is named after, disconnect.

## Extending DGram

Adding a new command takes three steps:

1. Create `commands/my_command` with a `#!/usr/bin/env -S uv run python` shebang and the standard `sys.path` bootstrap (copy it from any existing command).
2. Call `libs.dgram.get_client(tdata_path)` to obtain your `TelegramClient`, then reach for whichever Telethon call you need.
3. `chmod +x commands/my_command` and you have a new, first-class utility — no registration, no plugin system, nothing further to wire up.

## Security notes

- All Telegram traffic is forced through the Tor SOCKS5 proxy — there is no code path that reaches the internet directly.
- The Tor control port is guarded by a password (`libs/tor.CONTROL_PASSWORD`) and published to `127.0.0.1` only, never beyond the host.
- `tdata` folders and `.session` files are sensitive: they grant full account access. Keep them out of version control (see `.gitignore`) and off shared machines.
