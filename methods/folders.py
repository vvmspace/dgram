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
    interactive: bool = True,
) -> list[str]:
    client = await get_client(tdata_path, session_path, interactive)
    try:
        result = await client(GetDialogFiltersRequest())
        lines = []
        for folder in result.filters:
            if isinstance(folder, DialogFilterDefault):
                lines.append("default\tAll Chats")
                continue
            lines.append(
                f"{folder.id}\t{folder.title.text}\t+{len(folder.include_peers)}\t-{len(folder.exclude_peers)}"
            )
        return lines
    finally:
        await client.disconnect()
