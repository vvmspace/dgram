"""
Awaits an incoming message matching a pattern, optionally sending one
first. Initialises its own DGram client on every call.
"""

import asyncio
import re

from telethon import events

from libs.dgram import get_client, resolve_target


async def wait_for_message(
    pattern: str,
    timeout: float,
    conversation_id: str | None = None,
    message: str | None = None,
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
) -> dict:
    client = await get_client(tdata_path, session_path)
    try:
        found: "asyncio.Future" = asyncio.get_event_loop().create_future()

        entity = None
        if conversation_id is not None:
            entity = await client.get_entity(resolve_target(conversation_id))

        event_kwargs = {"pattern": re.compile(pattern, re.DOTALL).search}
        if entity is not None:
            event_kwargs["chats"] = entity

        @client.on(events.NewMessage(**event_kwargs))
        async def handler(event):
            if not found.done():
                found.set_result(event.message)

        if entity is not None and message is not None:
            await client.send_message(entity, message)

        found_message = await asyncio.wait_for(found, timeout=timeout)
        return {"date": found_message.date.isoformat(), "text": found_message.text}
    finally:
        await client.disconnect()
