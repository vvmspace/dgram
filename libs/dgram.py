"""
Establishes an authenticated Telethon session.

Where tdata_path is given explicitly, it is authoritative: it must exist,
or this is an error. Otherwise, where session_path is given explicitly, or
neither argument is given and the default tdata folder is absent, a bare
.session file is used - authenticating interactively (phone, code, and
password where 2FA is enabled) should it not yet exist or be authorised,
and saving the result there. Left entirely unspecified, the default tdata
folder takes precedence over the default session file.

Every connection is routed through the SOCKS5 proxy (dperson/torproxy in
Docker), listening on localhost:9050.
"""

from pathlib import Path

from opentele.api import API, UseCurrentSession
from opentele.td import TDesktop
from opentele.tl import TelegramClient
from telethon.tl.types import DialogFilterDefault

PROXY = ("socks5", "localhost", 9050)
TDATA_PATH = "tdata"
SESSION_PATH = ".session"


async def _connect_via_tdata(tdata_path: str, session_path: str, proxy) -> TelegramClient:
    tdesk = TDesktop(tdata_path)
    assert tdesk.isLoaded(), f"Unable to load tdata from {tdata_path!r}"

    client: TelegramClient = await tdesk.ToTelethon(
        session=session_path,
        flag=UseCurrentSession,
        proxy=proxy,
    )
    await client.connect()
    assert await client.is_user_authorized(), "Session is not authorised"
    return client


async def _connect_via_session(session_path: str, proxy) -> TelegramClient:
    client = TelegramClient(session_path, api=API.TelegramDesktop, proxy=proxy)
    await client.connect()
    if not await client.is_user_authorized():
        await client.start()
    return client


async def get_client(
    tdata_path: str | None = None,
    session_path: str | None = None,
    proxy=PROXY,
) -> TelegramClient:
    if tdata_path is not None:
        if not Path(tdata_path).is_dir():
            raise RuntimeError(f"No tdata folder found at {tdata_path!r}")
        return await _connect_via_tdata(tdata_path, session_path or SESSION_PATH, proxy)

    if session_path is not None:
        return await _connect_via_session(session_path, proxy)

    if Path(TDATA_PATH).is_dir():
        return await _connect_via_tdata(TDATA_PATH, SESSION_PATH, proxy)
    return await _connect_via_session(SESSION_PATH, proxy)


def resolve_target(value: str | None):
    """@username/@me -> str for Telethon; numeric id -> int."""
    if value is None:
        return None
    if value.lower() == "@me":
        return "me"
    if value.lstrip("-").isdigit():
        return int(value)
    return value


def find_dialog_filter(filters, value: str):
    """Find a chat folder (DialogFilter) by id or by exact title."""
    for folder in filters:
        if isinstance(folder, DialogFilterDefault):
            continue
        if value.isdigit() and folder.id == int(value):
            return folder
        if folder.title.text == value:
            return folder
    return None
