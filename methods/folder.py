"""
Lists the chats within a given folder. Initialises its own DGram client on
every call.
"""

from telethon.tl.functions.messages import GetDialogFiltersRequest

from libs.dgram import find_dialog_filter, get_client


async def _describe(client, peer) -> str:
    entity = await client.get_entity(peer)
    username = getattr(entity, "username", None)
    return f"@{username}" if username else str(entity.id)


async def list_folder_chats(
    folder_ref: str,
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
) -> list[dict]:
    client = await get_client(tdata_path, session_path)
    try:
        result = await client(GetDialogFiltersRequest())
        folder = find_dialog_filter(result.filters, folder_ref)
        if folder is None:
            raise ValueError(f"No such folder: {folder_ref!r}")

        lines = [{"chat": await _describe(client, peer), "excluded": False} for peer in folder.include_peers]
        lines += [{"chat": await _describe(client, peer), "excluded": True} for peer in folder.exclude_peers]
        return lines
    finally:
        await client.disconnect()
