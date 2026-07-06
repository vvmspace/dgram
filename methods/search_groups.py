"""
Searches Telegram's own global search for public groups. Initialises its
own DGram client on every call.
"""

from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.types import Channel, Chat

from libs.dgram import get_client


def _is_group(chat) -> bool:
    if isinstance(chat, Channel):
        return chat.megagroup
    return isinstance(chat, Chat)


async def search_groups(
    query: str,
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
) -> list[dict]:
    client = await get_client(tdata_path, session_path)
    try:
        result = await client(SearchRequest(q=query, limit=50))
        lines = []
        for chat in result.chats:
            if not _is_group(chat):
                continue
            username = getattr(chat, "username", None)
            handle = f"@{username}" if username else str(chat.id)
            lines.append({"id": chat.id, "handle": handle, "title": chat.title})
        return lines
    finally:
        await client.disconnect()
