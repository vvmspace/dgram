"""
Joins a group, channel or invite link. Initialises its own DGram client on
every call.
"""

import re

from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

from libs.dgram import get_client, resolve_target

INVITE_HASH_RE = re.compile(r"(?:joinchat/|\+)([\w-]+)$")


async def join(
    group: str,
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
    interactive: bool = True,
) -> None:
    client = await get_client(tdata_path, session_path, interactive)
    try:
        invite_match = INVITE_HASH_RE.search(group)
        if invite_match:
            await client(ImportChatInviteRequest(invite_match.group(1)))
        else:
            entity = await client.get_entity(resolve_target(group))
            await client(JoinChannelRequest(entity))
    finally:
        await client.disconnect()
