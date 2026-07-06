## DGram - a library comprising a set of CLI utilities for managing tdata accounts over a secured connection.

Should the file [AGENTS.local.md] exist, treat it as the authoritative, up-to-date version.

- `libs/dgram`: Accepts, as its parameter, the path to a `TDATA_PATH = "tdata"` folder, or a `SESSION_PATH = ".session"`, with optional defaults `PROXY = ("socks5", "localhost", 9050)`, and yields a TelegramClient instance. Every connection within this project is conducted through it.
- `methods`
-- ...
- `commands` - commands bearing shebangs, without file extensions, which wrap the methods found in `methods`
-- `wait [-p tdata / --path-to-tdata=tdata] PATTERN [-t 30/--timeout=30]  [-c/--conversation_id=] [-m / --message=]` - engages `libs/dgram` and awaits a message matching PATTERN for timeout seconds. Should both conversation_id and message be supplied, it first sends the message.
-- `messages [-p tdata / --path-to-tdata=tdata] [-l 20/--length=20]` [-c ALL/--conversation_id=ALL] [-s ASC | --sort ASC] - `libs/dgram` -> prints the most recent length messages (including outgoing ones) within dialogue conversation_id, or across all dialogues where none is specified.
-- `send_message [-p tdata / --path-to-tdata=tdata] @user/@group/@me/conversation_id "message"` - `libs/dgram` -> send message; should the account not yet belong to the group, it joins and awaits random(5,15) seconds
-- `join [-p tdata / --path-to-tdata=tdata] @group` - `libs/dgram` -> joins the group
-- `leave [-p tdata / --path-to-tdata=tdata] @group` - `libs/dgram` -> leaves the group
-- `conversations [-p tdata / --path-to-tdata=tdata]` - `libs/dgram` -> lists dialogues/groups/channels
-- `group_create [-p tdata / --path-to-tdata=tdata] "Group name" @gr0upUs3rnam3` - `libs/dgram` -> creates a group, public @gr0upUs3rnam3
-- `group_invite [-p tdata / --path-to-tdata=tdata] @username/id @groupname/id` - `libs/dgram` -> invites a user into the group
-- `group_delete [-p tdata / --path-to-tdata=tdata] @gr0upUs3rnam3` - `libs/dgram` -> deletes the group
-- `group_clean_joins [-p tdata / --path-to-tdata=tdata] [-l 20/--length=20] @groupname` - `libs/dgram` -> deletes up to length "User joined the group" service messages
-- `search_groups [-p tdata / --path-to-tdata=tdata] "query"` - `libs/dgram` -> searches for groups by way of Telegram's own search
-- `folders [-p tdata / --path-to-tdata=tdata]` - `libs/dgram` -> lists chat folders: id, title, include/exclude counts
-- `folder [-p tdata / --path-to-tdata=tdata] <id|"Title">` - `libs/dgram` -> lists the chats within the given folder
-- `folder_add [-p tdata / --path-to-tdata=tdata] <id|"Title"> @chat` - `libs/dgram` -> adds a chat to the folder's list
-- `folder_remove [-p tdata / --path-to-tdata=tdata] <id|"Title"> @chat` - `libs/dgram` -> removes a chat from the folder's list
-- `email_get [-p tdata / --path-to-tdata=tdata]` - `libs/dgram` -> gets the login-email setting (a masked pattern)
-- `email_set [-p tdata / --path-to-tdata=tdata] you@example.com` - `libs/dgram` -> sets the login-email setting, prompting for the confirmation code
-- `session [-p tdata / --path-to-tdata=tdata] [-s .session / --session=.session]` - information about the session

-- `up` - brings up (recreates) the torproxy Docker container, publishing the SOCKS5 and control ports, with the control-port password (`libs/tor.CONTROL_PASSWORD`, shared with `switch`)
-- `down` - stops and removes the torproxy Docker container; the volumes holding Tor's data are preserved
-- `switch [-h localhost / --host=localthost] [-p 9050 / --port=9050] [-c 9051 / --control-port=9051]` - checks ip address using socks5://host:port proxy -> switches Tor identity -> polls the ip address using socks5://host:port until it actually changes. Strict requirement: the command must wait for the IP to change and must not exit without it; if the IP has not changed within a minute, it resends the identity-change signal.
-- `help` - lists the commands

- `README.md` - lavishly written, engaging and persuasive for the user, optimised for SEO and GEO discovery by prospective users. It ought to demonstrate the ease of use and the ease of extension.

## Commands common parameters:

- `[-p tdata / --path-to-tdata=tdata] [-s .session / --session=.session]` - an optional parameter giving the path to the tdata folder or to a session, each with the defaults shown. Order of checking: tdata -> .session. Where `--path-to-tdata` is given explicitly and does not exist, this is an error. Otherwise, where `--session` (whether given explicitly, e.g. without `--path-to-tdata`, or left at its default) does not exist, the user is invited to authenticate: `phone/email` -> `code` `[-> password, where 2FA is enabled]`, and the resulting session is saved there. An explicit `--session` takes precedence over a merely-default `tdata` folder: should the given session not yet exist, authentication is offered even where the default `tdata` folder is present. By default, `tdata` and `.session` are sought in the working directory.

Language within the code: posh UK English only
