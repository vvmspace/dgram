"""
Lists chat folders. Initialises its own DGram client on every call.
"""

from telethon.tl.functions.messages import GetDialogFiltersRequest
from telethon.tl.types import DialogFilterDefault

from libs.dgram import get_client


async def list_folders(
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
) -> list[dict]:
    client = await get_client(tdata_path, session_path)
    try:
        result = await client(GetDialogFiltersRequest())
        lines = []
        for folder in result.filters:
            if isinstance(folder, DialogFilterDefault):
                lines.append({"id": "default", "title": "All Chats"})
                continue
            lines.append({
                "id": folder.id,
                "title": folder.title.text,
                "include_count": len(folder.include_peers),
                "exclude_count": len(folder.exclude_peers),
            })
        return lines
    finally:
        await client.disconnect()
