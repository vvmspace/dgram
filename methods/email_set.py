"""
Sets, or changes, the account's login email, prompting interactively for
the confirmation code Telegram sends to that address. Initialises its own
DGram client on every call.
"""

from telethon.tl.functions.account import SendVerifyEmailCodeRequest, VerifyEmailRequest
from telethon.tl.types import EmailVerificationCode, EmailVerifyPurposeLoginChange

from libs.dgram import get_client


async def set_email(
    email: str,
    *,
    code_callback=input,
    tdata_path: str | None = None,
    session_path: str | None = None,
) -> None:
    client = await get_client(tdata_path, session_path)
    try:
        purpose = EmailVerifyPurposeLoginChange()
        await client(SendVerifyEmailCodeRequest(purpose=purpose, email=email))
        code = code_callback(f"Enter the code Telegram sent to {email}: ")
        await client(VerifyEmailRequest(purpose=purpose, verification=EmailVerificationCode(code=code)))
    finally:
        await client.disconnect()
