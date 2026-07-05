## DGram - a library comprising a set of CLI utilities for managing tdata accounts over a secured connection.

Should the file [AGENTS.local.md] exist, treat it as the authoritative, up-to-date version.

- `libs/dgram`: Accepts, as its parameter, the path to a `tdata` folder, with optional defaults `PROXY = ("socks5", "localhost", 9050)`, and yields a TelegramClient instance. Every connection within this project is conducted through it.
- `commands` - commands bearing shebangs, without file extensions
-- `wait path/to/tdata PATTERN [-t 30/--timeout=30]  [-c/--conversation_id=] [-m / --message=]` - engages `libs/dgram` and awaits a message matching PATTERN for timeout seconds. Should both conversation_id and message be supplied, it first sends the message.
-- `messages path/to/tdata [-l 20/--length=20]` [-c ALL/--conversation_id=ALL] [-s ASC | --sort ASC] - `libs/dgram` -> prints the most recent length messages (including outgoing ones) within dialogue conversation_id, or across all dialogues where none is specified.
-- `send_message path/to/tdata @user/@group/@me/conversation_id "message"` - `libs/dgram` -> send message; should the account not yet belong to the group, it joins and awaits random(5,15) seconds
-- `join path/to/tdata @group` - `libs/dgram` -> joins the group
-- `leave path/to/tdata @group` - `libs/dgram` -> leaves the group
-- `conversations path/to/tdata` - `libs/dgram` -> lists dialogues/groups/channels
-- `group_create path/to/tdata "Group name" @gr0upUs3rnam3` - `libs/dgram` -> creates a group, public @gr0upUs3rnam3
-- `group_invite path/to/tdata @username/id @groupname/id` - `libs/dgram` -> invites a user into the group
-- `group_delete path/to/tdata @gr0upUs3rnam3` - `libs/dgram` -> deletes the group
-- `search_groups path/to/tdata "query"` - `libs/dgram` -> searches for groups by way of Telegram's own search

-- `up` - brings up (recreates) the torproxy Docker container, publishing the SOCKS5 and control ports, with the control-port password (`libs/tor.CONTROL_PASSWORD`, shared with `switch`)
-- `down` - stops and removes the torproxy Docker container; the volumes holding Tor's data are preserved
-- `switch` [-h localhost / --host=localthost] [-p 9050 / --port=9050] [-c 9051 / --control-port=9051] - checks ip address using socks5://host:port proxy -> switches Tor identity -> checks new ip address using socks5://host:port
-- `help` - lists the commands

- `README.md` - lavishly written, engaging and persuasive for the user, optimised for SEO and GEO discovery by prospective users. It ought to demonstrate the ease of use and the ease of extension.

Language within the code: posh UK English only
