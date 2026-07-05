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
    interactive: bool = True,
) -> list[str]:
    client = await get_client(tdata_path, session_path, interactive)
    try:
        result = await client(GetDialogFiltersRequest())
        folder = find_dialog_filter(result.filters, folder_ref)
        if folder is None:
            raise ValueError(f"No such folder: {folder_ref!r}")

        lines = [await _describe(client, peer) for peer in folder.include_peers]
        lines += [f"-{await _describe(client, peer)}" for peer in folder.exclude_peers]
        return lines
    finally:
        await client.disconnect()
