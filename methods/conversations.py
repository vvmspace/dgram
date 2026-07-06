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
) -> list[str]:
    client = await get_client(tdata_path, session_path)
    try:
        lines = []
        async for dialog in client.iter_dialogs():
            lines.append(f"{dialog.id}\t{_kind(dialog)}\t{dialog.name}")
        return lines
    finally:
        await client.disconnect()
