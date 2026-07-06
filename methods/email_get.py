"""
Retrieves the account's login-email setting. Telegram only ever exposes a
masked pattern (e.g. "a**e@e***e.com"), never the address in full.
Initialises its own DGram client on every call.
"""

from telethon.tl.functions.account import GetPasswordRequest

from libs.dgram import get_client


async def get_email(
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
) -> str | None:
    client = await get_client(tdata_path, session_path)
    try:
        password = await client(GetPasswordRequest())
        return password.login_email_pattern
    finally:
        await client.disconnect()
