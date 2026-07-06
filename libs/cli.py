"""
Shared argparse wiring for the -p/--path-to-tdata and -s/--session options
common to every account-facing command.

For security, commands never hold a TelegramClient themselves: each
`methods` function initialises its own via libs.dgram.get_client. This
module merely turns parsed CLI arguments into the keyword arguments that
call expects. An explicit, non-existent --path-to-tdata is treated as an
error, since a tdata folder cannot be conjured up by logging in - but a
missing --session (explicit or default) simply launches an interactive
login, which then saves its session there.
"""

import argparse

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


def client_kwargs(args: argparse.Namespace) -> dict:
    return {
        "tdata_path": args.path_to_tdata,
        "session_path": args.session,
        "interactive": args.path_to_tdata is None,
    }
