# 📡 DGram

**Command your own Telegram accounts from the terminal — securely, elegantly, and without a single re-login.**

DGram is a compact Python toolkit that turns a Telegram Desktop `tdata` folder into a fully-fledged, scriptable Telegram session. No QR codes, no verification codes, no fumbling about with API credentials by hand: point a command at your `tdata` folder and it converts, authenticates, and connects — every single time, routed through Tor for good measure.

Whether you are orchestrating a personal userbot, wiring up bespoke Telegram automation, or simply prefer a keyboard to a touchscreen, DGram gives you a tidy set of shell-ready commands for reading messages, sending them, and managing groups — all built atop [Telethon](https://github.com/LonamiWebs/Telethon) and [opentele](https://github.com/thedemons/opentele).

## 🎩 Why DGram

- 🔑 **Zero re-authentication.** Reuses your existing Telegram Desktop session (`tdata`) directly — the account stays logged in, exactly as you left it.
- 🆕 **No account yet? No matter.** Where neither a `tdata` folder nor a `.session` file can be found, DGram invites you to log in there and then — phone, code, and password where 2FA is enabled — and remembers you for next time.
- 🧅 **Private by design.** Every connection — to Telegram, and nowhere else — is routed through a local Tor SOCKS5 proxy, courtesy of [`dperson/torproxy`](https://hub.docker.com/r/dperson/torproxy) in Docker.
- 🎯 **One command, one job.** Each utility does a single thing well: no bloated multi-purpose binary, no configuration files to wrangle.
- 🧩 **Delightfully easy to extend.** Every command is a slim, shebanged wrapper around a `methods` function, built on one shared client factory (`libs/dgram.get_client`). Adding a new capability is a matter of minutes, not an afternoon.
- 🎈 **Genuinely portable.** No installation, no daemons, no background services beyond the proxy itself. Run a command; it does its work and exits.

## 🧰 Requirements

- 🐍 Python 3.12 or newer, managed via [`uv`](https://docs.astral.sh/uv/)
- 🐳 Docker, for the bundled Tor proxy
- 📂 Either a `tdata` folder from an existing Telegram Desktop installation, a `.session` file, or simply a phone number to hand — DGram will log in interactively if neither file exists yet

## 🚀 Quickstart

Bring the Tor proxy up, then talk to Telegram through it:

```sh
commands/up                        # starts the torproxy container
commands/conversations             # lists every dialogue, group and channel
commands/messages -l 10            # prints the ten most recent messages
commands/send_message @friend "Good evening!"
commands/down                      # stops the proxy once you are done
```

Every account-facing command follows the very same shape: `commands/<name> [-p path/to/tdata] [-s path/to/.session] [arguments…]`. Left unspecified, `-p`/`-s` default to `tdata`/`.session` in the working directory — and if neither exists, the command simply asks you to log in. No installation step, no virtual environment to activate by hand — `uv` handles all of that via the shebang line at the top of each script.

## 📖 Command reference

| | Command | Purpose |
|---|---|---|
| 🌐 | `up` | Brings up (or recreates) the Tor proxy container, publishing the SOCKS5 and control ports |
| 🛑 | `down` | Stops the Tor proxy container, keeping its data volumes intact |
| 🔄 | `switch [-h host] [-p port] [-c control-port]` | Requests a fresh Tor identity and waits, however long it takes, until the exit IP address actually changes (resending the request every minute) |
| 📇 | `conversations [-p tdata] [-s .session]` | Lists dialogues, groups and channels |
| 💬 | `messages [-p tdata] [--session] [-l length] [-c conversation_id] [-s ASC\|DESC]` | Prints recent messages, including your own, from one dialogue or across the lot |
| ✉️ | `send_message [-p tdata] [-s .session] target "text"` | Sends a message; joins the target group first if you are not yet a member |
| ⏳ | `wait [-p tdata] [-s .session] PATTERN [-t timeout] [-c conversation_id] [-m message]` | Waits for an incoming message matching a pattern, optionally sending one first |
| ➕ | `join [-p tdata] [-s .session] @group` | Joins a group, channel or invite link |
| ➖ | `leave [-p tdata] [-s .session] @group` | Leaves a group or channel |
| 🏗️ | `group_create [-p tdata] [-s .session] "Title" @username` | Creates a new public supergroup |
| 🤝 | `group_invite [-p tdata] [-s .session] @user @group` | Invites a user into a group |
| 🗑️ | `group_delete [-p tdata] [-s .session] @group` | Deletes a group |
| 🔍 | `search_groups [-p tdata] [-s .session] "query"` | Searches Telegram's own directory for public groups |
| 📧 | `email_get [-p tdata] [-s .session]` | Gets the login-email setting (a masked pattern) |
| 📨 | `email_set [-p tdata] [-s .session] you@example.com` | Sets the login-email setting, prompting for the confirmation code |
| 🪪 | `session [-p tdata] [-s .session]` | Prints information about the authenticated account and session |
| 🗂️ | `folders [-p tdata] [-s .session]` | Lists chat folders, with their include/exclude counts |
| 📁 | `folder [-p tdata] [-s .session] <id\|"Title">` | Lists the chats within a given folder |
| ➕ | `folder_add [-p tdata] [-s .session] <id\|"Title"> @chat` | Adds a chat to a folder's list |
| ➖ | `folder_remove [-p tdata] [-s .session] <id\|"Title"> @chat` | Removes a chat from a folder's list |
| 🆘 | `help` | Lists every command, with its usage synopsis |

`-p`/`--path-to-tdata` and `-s`/`--session` (`messages` uses `--session` only, since `-s` there means `--sort`) default to `tdata` and `.session` in the working directory. Run any command with `--help` for its full argument list.

## 🏛️ Architecture, in brief

```
libs/dgram.py   -> get_client(tdata_path, session_path)   resolves tdata -> .session -> interactive login, over Tor
libs/cli.py     -> shared -p/--path-to-tdata and -s/--session argparse wiring
libs/tor.py     -> shared Tor proxy/container settings, used by up, down and switch
methods/*       -> one module per capability, each initialising its own client and returning data rather than printing it
commands/*      -> one shebanged script per capability: parse arguments, call into methods, print the result
```

Every command reads top to bottom without surprises, and stays a thin shell around its `methods` counterpart — which is where the logic actually lives, and where it can be reused or tested independently of any CLI concerns. Notably, no client is ever passed between the two: for security, each `methods` function initialises its own DGram session rather than accepting one ready-made, so a command can never hand it a client from an untrusted or unexpected source.

## 🧩 Extending DGram

Adding a new command takes four steps:

1. 🧠 Write the logic as a function in `methods/my_command.py`, accepting `tdata_path`/`session_path`/`interactive` keyword arguments and initialising its own client via `libs.dgram.get_client` — never accept a client as a parameter. Return data rather than printing it.
2. 📄 Create `commands/my_command` with a `#!/usr/bin/env -S uv run python` shebang and the standard `sys.path` bootstrap (copy it from any existing command).
3. 🔌 Call `libs.cli.add_client_arguments(parser)` for the standard `-p`/`-s` options, then call your `methods` function with `**libs.cli.client_kwargs(args)`.
4. ✅ `chmod +x commands/my_command` and you have a new, first-class utility — no registration, no plugin system, nothing further to wire up.

## 🔐 Security notes

- 🧅 All Telegram traffic is forced through the Tor SOCKS5 proxy — there is no code path that reaches the internet directly.
- 🔑 The Tor control port is guarded by a password (`libs/tor.CONTROL_PASSWORD`) and published to `127.0.0.1` only, never beyond the host.
- ⚠️ `tdata` folders and `.session` files are sensitive: they grant full account access. Keep them out of version control (see `.gitignore`) and off shared machines.
- 🚫 No `methods` function ever accepts a pre-built client: each initialises and tears down its own, so a client can never be smuggled in from an untrusted caller.
