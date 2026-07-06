"""
Creates a public supergroup. Initialises its own DGram client on every
call.
"""

from telethon.tl.functions.channels import CreateChannelRequest, UpdateUsernameRequest

from libs.dgram import get_client


async def create_group(
    title: str,
    username: str,
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
):
    client = await get_client(tdata_path, session_path)
    try:
        result = await client(CreateChannelRequest(title=title, about="", megagroup=True))
        channel = result.chats[0]
        username = username.lstrip("@")
        await client(UpdateUsernameRequest(channel, username))
        return channel, username
    finally:
        await client.disconnect()
