"""
Invites a user into a group or channel. Initialises its own DGram client on
every call.
"""

from telethon.tl.functions.channels import InviteToChannelRequest

from libs.dgram import get_client, resolve_target


async def invite(
    user: str,
    group: str,
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
    interactive: bool = True,
) -> None:
    client = await get_client(tdata_path, session_path, interactive)
    try:
        user_entity = await client.get_entity(resolve_target(user))
        group_entity = await client.get_entity(resolve_target(group))
        await client(InviteToChannelRequest(group_entity, [user_entity]))
    finally:
        await client.disconnect()
