import asyncio
import logging
import struct
from asyncio import Queue
from concurrent.futures import CancelledError

import bitstring


REQUEST_SIZE = 2**14


class ProtocolError(BaseException):
    pass


class PeerConnection:
    """
    A peer Connection used to download and upload pieces.

    The peer connection will consume one available peer from the given queue.
    Based on the peer detail the peerConnection will try to open a connection and perform A Bittorrent handshake

    """