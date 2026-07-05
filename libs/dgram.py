"""
Establishes an authenticated Telethon session, resolved in order from: a
tdata (Telegram Desktop) folder, a bare .session file, or - failing both -
an interactive login (phone, code, and password where 2FA is enabled),
whose resulting session is then saved to session_path.

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


async def get_client(
    tdata_path: str | None = None,
    session_path: str | None = None,
    interactive: bool = True,
    proxy=PROXY,
) -> TelegramClient:
    tdata_path = tdata_path or TDATA_PATH
    session_path = session_path or SESSION_PATH

    if Path(tdata_path).is_dir():
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

    client = TelegramClient(session_path, api=API.TelegramDesktop, proxy=proxy)
    await client.connect()
    if not await client.is_user_authorized():
        if not interactive:
            raise RuntimeError(
                f"Neither a tdata folder at {tdata_path!r} nor an authorised "
                f"session at {session_path!r} could be found"
            )
        await client.start()
    return client


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
