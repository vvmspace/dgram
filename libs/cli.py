"""
Shared argparse wiring for the -p/--path-to-tdata, -s/--session and --json
options common to every account-facing command.

For security, commands never hold a TelegramClient themselves: each
`methods` function initialises its own via libs.dgram.get_client, and
returns plain data (or nothing at all) rather than a Telethon object -
which is what lets emit() below serialise it to JSON without any
command-specific knowledge. This module merely turns parsed CLI arguments
into the keyword arguments that call expects - passing None through for
whichever of --path-to-tdata and --session was left unspecified, so
libs.dgram.get_client can tell an explicit choice apart from its own
default.
"""

import argparse
import json
from typing import Callable

from libs.dgram import SESSION_PATH, TDATA_PATH


def add_client_arguments(parser: argparse.ArgumentParser, session_short: str | None = "-s") -> None:
    parser.add_argument(
        "-p", "--path-to-tdata", dest="path_to_tdata", default=None,
        help=f"Path to the tdata folder (default: {TDATA_PATH!r})",
    )
    session_flags = [flag for flag in (session_short, "--session") if flag]
    parser.add_argument(
        *session_flags, dest="session", default=None,
        help=f"Path to a .session file (default: {SESSION_PATH!r})",
    )
    parser.add_argument(
        "--json", dest="json_path", default=None, metavar="PATH",
        help="Write the result as JSON to PATH, instead of printing it",
    )


def client_kwargs(args: argparse.Namespace) -> dict:
    return {
        "tdata_path": args.path_to_tdata,
        "session_path": args.session,
    }


def emit(data, json_path: str | None, formatter: Callable[..., None]) -> None:
    """
    Where json_path is given, writes data to it as JSON; otherwise calls
    formatter(data) to print the result in the command's usual
    human-readable form.
    """
    if json_path:
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2, default=str)
        print(f"Written to {json_path}")
    else:
        formatter(data)
