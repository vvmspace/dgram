"""
Lists dialogues, groups and channels. Initialises its own DGram client on
every call.
"""

from libs.dgram import get_client


def _kind(dialog) -> str:
    if dialog.is_user:
        return "user"
    if dialog.is_channel:
        return "channel"
    if dialog.is_group:
        return "group"
    return "unknown"


async def list_conversations(
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
) -> list[dict]:
    client = await get_client(tdata_path, session_path)
    try:
        lines = []
        async for dialog in client.iter_dialogs():
            lines.append({"id": dialog.id, "kind": _kind(dialog), "name": dialog.name})
        return lines
    finally:
        await client.disconnect()
