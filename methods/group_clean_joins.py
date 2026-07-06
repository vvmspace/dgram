"""
Deletes "User joined the group" service messages from a group, up to
length of them. Initialises its own DGram client on every call.
"""

from telethon.tl.types import (
    MessageActionChatAddUser,
    MessageActionChatJoinedByLink,
    MessageActionChatJoinedByRequest,
)

from libs.dgram import get_client, resolve_target

JOIN_ACTIONS = (
    MessageActionChatAddUser,
    MessageActionChatJoinedByLink,
    MessageActionChatJoinedByRequest,
)


async def clean_joins(
    group: str,
    length: int,
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
) -> dict:
    client = await get_client(tdata_path, session_path)
    try:
        entity = await client.get_entity(resolve_target(group))

        message_ids = []
        async for message in client.iter_messages(entity):
            if isinstance(getattr(message, "action", None), JOIN_ACTIONS):
                message_ids.append(message.id)
                if len(message_ids) >= length:
                    break

        if message_ids:
            await client.delete_messages(entity, message_ids)

        return {"group": group, "deleted": len(message_ids)}
    finally:
        await client.disconnect()
