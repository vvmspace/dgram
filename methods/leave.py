"""
Leaves a group or channel. Initialises its own DGram client on every call.
"""

from telethon.tl.functions.channels import LeaveChannelRequest

from libs.dgram import get_client, resolve_target


async def leave(
    group: str,
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
) -> dict:
    client = await get_client(tdata_path, session_path)
    try:
        entity = await client.get_entity(resolve_target(group))
        await client(LeaveChannelRequest(entity))
        return {"group": group}
    finally:
        await client.disconnect()
