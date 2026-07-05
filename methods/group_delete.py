"""
Deletes a group or channel. Initialises its own DGram client on every call.
"""

from telethon.tl.functions.channels import DeleteChannelRequest

from libs.dgram import get_client, resolve_target


async def delete_group(
    group: str,
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
    interactive: bool = True,
) -> None:
    client = await get_client(tdata_path, session_path, interactive)
    try:
        entity = await client.get_entity(resolve_target(group))
        await client(DeleteChannelRequest(entity))
    finally:
        await client.disconnect()
