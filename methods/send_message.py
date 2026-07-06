"""
Sends a message, optionally with one or more attached files/images, joining
the target channel/group first (with a short random delay) where the
account is not yet a member. Initialises its own DGram client on every
call.
"""

import asyncio
import random

from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest, JoinChannelRequest
from telethon.tl.types import Channel

from libs.dgram import get_client, resolve_target


async def _is_member(client, channel: Channel) -> bool:
    try:
        await client(GetParticipantRequest(channel, "me"))
        return True
    except UserNotParticipantError:
        return False


async def send_message(
    target: str,
    text: str,
    files: list[str] | None = None,
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
) -> dict:
    client = await get_client(tdata_path, session_path)
    try:
        entity = await client.get_entity(resolve_target(target))

        if isinstance(entity, Channel) and not await _is_member(client, entity):
            await client(JoinChannelRequest(entity))
            await asyncio.sleep(random.uniform(5, 15))

        file = (files[0] if len(files) == 1 else files) if files else None
        sent = await client.send_message(entity, text, file=file)
        return {"date": sent.date.isoformat(), "target": target, "text": sent.text, "files": files or []}
    finally:
        await client.disconnect()
