"""
Converts tdata (Telegram Desktop) into a Telethon session.

Every connection is routed through the SOCKS5 proxy (dperson/torproxy in
Docker), listening on localhost:9050.
"""

from pathlib import Path

from opentele.api import UseCurrentSession
from opentele.td import TDesktop
from opentele.tl import TelegramClient
from telethon.tl.types import DialogFilterDefault

PROXY = ("socks5", "localhost", 9050)


async def get_client(
    tdata_path: str = "tdata",
    session_path: str | None = None,
    proxy=PROXY,
) -> TelegramClient:
    if session_path is None:
        session_path = str(Path(tdata_path.rstrip("/\\")).with_suffix(".session"))

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
