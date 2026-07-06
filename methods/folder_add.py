"""
Adds a chat to a folder's list. Initialises its own DGram client on every
call.
"""

from telethon import utils
from telethon.tl.functions.messages import GetDialogFiltersRequest, UpdateDialogFilterRequest

from libs.dgram import find_dialog_filter, get_client, resolve_target


async def add_to_folder(
    folder_ref: str,
    chat: str,
    *,
    tdata_path: str | None = None,
    session_path: str | None = None,
) -> None:
    client = await get_client(tdata_path, session_path)
    try:
        result = await client(GetDialogFiltersRequest())
        folder = find_dialog_filter(result.filters, folder_ref)
        if folder is None:
            raise ValueError(f"No such folder: {folder_ref!r}")

        target_peer = await client.get_input_entity(resolve_target(chat))
        target_id = utils.get_peer_id(target_peer)

        folder.exclude_peers = [p for p in folder.exclude_peers if utils.get_peer_id(p) != target_id]
        if not any(utils.get_peer_id(p) == target_id for p in folder.include_peers):
            folder.include_peers.append(target_peer)

        await client(UpdateDialogFilterRequest(id=folder.id, filter=folder))
    finally:
        await client.disconnect()
