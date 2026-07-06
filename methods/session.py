"""
Retrieves information about the authenticated account and session.
Initialises its own DGram client on every call.
"""

from libs.dgram import get_client


async def get_session_info(
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
) -> list[str]:
    client = await get_client(tdata_path, session_path)
    try:
        me = await client.get_me()
        name = " ".join(part for part in (me.first_name, me.last_name) if part)
        return [
            f"id: {me.id}",
            f"username: @{me.username}" if me.username else "username: (none)",
            f"phone: +{me.phone}" if me.phone else "phone: (hidden)",
            f"name: {name}" if name else "name: (none)",
            f"premium: {bool(getattr(me, 'premium', False))}",
            f"dc: {client.session.dc_id}",
        ]
    finally:
        await client.disconnect()
