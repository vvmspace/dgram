"""
Lists unread incoming messages, from one dialogue or across the lot,
without marking them as read: only messages.getHistory (via
client.iter_messages) and messages.getPeerDialogs are used, neither of
which acknowledges anything - unlike client.send_read_acknowledge, which
this module never calls. Initialises its own DGram client on every call.

In ALL mode, unread dialogues are fetched concurrently (bounded by a
semaphore) rather than one after another, since a strictly sequential
crawl over every unread dialogue can otherwise take a very long time on
an account subscribed to hundreds of channels. Two limits bound the work
regardless: chat_limit caps how many unread messages are pulled from any
one dialogue (a single very active group can otherwise have thousands of
unread messages sitting behind read_inbox_max_id), and total_limit caps
the overall count collected across every dialogue combined. dm_only
restricts ALL mode to private (one-to-one) dialogues, skipping groups and
channels entirely.
"""

import asyncio
from typing import Callable

from telethon.tl.functions.messages import GetPeerDialogsRequest
from telethon.tl.types import User

from libs.dgram import get_client, resolve_target
from methods.messages import _label

CONCURRENCY = 8


class _Budget:
    def __init__(self, remaining: int):
        self.remaining = remaining


async def _unread_messages(client, me_id: int, entity, dialog_id: int, in_group: bool, chat_username, read_inbox_max_id: int, chat_limit: int, budget: _Budget) -> list[tuple]:
    rows = []
    per_chat = min(chat_limit, budget.remaining)
    if per_chat <= 0:
        return rows

    async for message in client.iter_messages(entity, min_id=read_inbox_max_id, limit=per_chat):
        if message.out:
            continue
        if budget.remaining <= 0:
            break
        label = await _label(message, me_id, chat_username, dialog_id, in_group)
        rows.append((message.date, {"date": message.date.isoformat(), "label": label, "text": message.text}))
        budget.remaining -= 1
    return rows


async def list_unread(
    conversation_id: str = "ALL",
    limit: int | None = None,
    *,
    chat_limit: int = 10,
    total_limit: int = 1000,
    dm_only: bool = False,
    on_progress: Callable[[int, int, str], None] | None = None,
    tdata_path: str | None = None,
    session_path: str | None = None,
) -> list[dict]:
    client = await get_client(tdata_path, session_path)
    try:
        me = await client.get_me()
        rows: list[tuple] = []
        budget = _Budget(total_limit)

        if conversation_id == "ALL":
            unread_dialogs = []
            async for dialog in client.iter_dialogs():
                if dm_only and not dialog.is_user:
                    continue
                if dialog.unread_count > 0:
                    unread_dialogs.append(dialog)
                    if limit is not None and len(unread_dialogs) >= limit:
                        break

            total = len(unread_dialogs)
            done = 0
            semaphore = asyncio.Semaphore(CONCURRENCY)

            async def _process(dialog):
                nonlocal done
                async with semaphore:
                    in_group = not dialog.is_user
                    chat_username = getattr(dialog.entity, "username", None)
                    result = await _unread_messages(
                        client, me.id, dialog.entity, dialog.id, in_group, chat_username,
                        dialog.dialog.read_inbox_max_id, chat_limit, budget,
                    )
                done += 1
                if on_progress:
                    on_progress(done, total, dialog.name)
                return result

            for result in await asyncio.gather(*(_process(dialog) for dialog in unread_dialogs)):
                rows += result
        else:
            try:
                entity = await client.get_entity(resolve_target(conversation_id))
            except ValueError:
                raise ValueError(
                    f"Could not find dialogue {conversation_id!r}: "
                    "the id is unknown to this session (never encountered in any dialogue)."
                ) from None

            input_peer = await client.get_input_entity(entity)
            peer_dialogs = await client(GetPeerDialogsRequest(peers=[input_peer]))
            dialog = peer_dialogs.dialogs[0]

            if dialog.unread_count > 0:
                in_group = not isinstance(entity, User)
                chat_username = getattr(entity, "username", None)
                rows += await _unread_messages(
                    client, me.id, entity, entity.id, in_group, chat_username,
                    dialog.read_inbox_max_id, chat_limit, budget,
                )

        rows.sort(key=lambda row: row[0])
        return [item for _, item in rows]
    finally:
        await client.disconnect()
