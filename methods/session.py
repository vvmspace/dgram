"""
Retrieves information about the authenticated account and session.
Initialises its own DGram client on every call.
"""

from libs.dgram import get_client


async def get_session_info(
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
) -> dict:
    client = await get_client(tdata_path, session_path)
    try:
        me = await client.get_me()
        name = " ".join(part for part in (me.first_name, me.last_name) if part)
        return {
            "id": me.id,
            "username": me.username,
            "phone": me.phone,
            "name": name or None,
            "premium": bool(getattr(me, "premium", False)),
            "dc": client.session.dc_id,
        }
    finally:
        await client.disconnect()
