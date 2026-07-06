"""
Retrieves recent messages, from one dialogue or across the lot.
Initialises its own DGram client on every call.

Sender label format:
    Me (id) to @user/@group(chat_id):            - an outgoing message
    @user(user_id):                              - incoming, within a private dialogue
    @user in @group(group_id/user_id):           - incoming, within a group/channel
"""

from telethon.tl.types import User

from libs.dgram import get_client, resolve_target


async def _label(message, me_id: int, chat_username: str | None, chat_id: int | None, in_group: bool) -> str:
    chat_part = f"@{chat_username}" if chat_username else str(chat_id)

    if message.out or message.sender_id == me_id:
        return f"Me ({message.sender_id}) to {chat_part}({chat_id})"

    sender = await message.get_sender()
    username = getattr(sender, "username", None)
    user_part = f"@{username}" if username else str(message.sender_id)

    if not in_group:
        return f"{user_part}({message.sender_id})"

    return f"{user_part} in {chat_part}({chat_id}/{message.sender_id})"


async def get_messages(
    conversation_id: str,
    length: int,
    sort: str,
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
) -> list[dict]:
    client = await get_client(tdata_path, session_path)
    try:
        me = await client.get_me()
        rows: list[tuple] = []

        if conversation_id == "ALL":
            async for dialog in client.iter_dialogs():
                in_group = not dialog.is_user
                chat_username = getattr(dialog.entity, "username", None)
                async for message in client.iter_messages(dialog, limit=length):
                    label = await _label(message, me.id, chat_username, dialog.id, in_group)
                    rows.append((message.date, {"date": message.date.isoformat(), "label": label, "text": message.text}))

            rows.sort(key=lambda row: row[0], reverse=True)
            rows = rows[:length]
        else:
            try:
                entity = await client.get_entity(resolve_target(conversation_id))
            except ValueError:
                raise ValueError(
                    f"Could not find dialogue {conversation_id!r}: "
                    "the id is unknown to this session (never encountered in any dialogue)."
                ) from None
            in_group = not isinstance(entity, User)
            chat_username = getattr(entity, "username", None)
            async for message in client.iter_messages(entity, limit=length):
                label = await _label(message, me.id, chat_username, entity.id, in_group)
                rows.append((message.date, {"date": message.date.isoformat(), "label": label, "text": message.text}))

        rows.sort(key=lambda row: row[0], reverse=(sort == "DESC"))
        return [item for _, item in rows]
    finally:
        await client.disconnect()
