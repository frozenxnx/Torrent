import argparse
import asyncio
import signal
import logging

from concurrent.futures import CancelledError

from Files.Torrent import Torrent
from Files.client import TorrentClient

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('torrent',
                        help='the .torrent to download')
    parser.add_argument('-v','--verbose',action='store_true',
                        help='enable verbose ouput')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level= logging.INFO)

    loop = asyncio.get_event_loop()
    client = TorrentClient(Torrent(args.torrent))
    task = loop.create_task(client.start())

    signal.signal(signal.SIGINT,signal_handler)

    try:
        loop.run_until_complete(task)
    except CancelledError:
        logging.warning('Event loop was cancelled')