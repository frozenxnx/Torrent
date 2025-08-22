import aiohttp
import asyncio
from  struct import unpack
import socket
import logging
from urllib.parse import urlencode

from . import bencoding

class Tracker:
    """
    Represents a connection to a tracker for a given torrent that is under downloading or seeding state
    """
    def __init__(self, torrent):
        self._session = session
        self.torrent = torrent
        self.peer_id = calculate_peer_id()
        self.http_client = aiohttp.ClientSession()


    async def connect(self,
                     first: bool = None,
                      uplaoded:int =0,
                      downloaded:int =0):
        """
         Makes the announce call to the tracker to update with our statistics
        as well as get a list of available peers to connect to.

        If the call was successful, the list of peers will be updated as a
        result of calling this function.

        :param first: Whether or not this is the first announce call
        :param uploaded: The total number of bytes uploaded
        :param downloaded: The total number of bytes downloaded
        """

        params = {
            'info_hash': self.torrent.info_hash,
            'peer_id': self.peer_id,
            'port': 6889,
            'uploaded':uploaded,
            'downloaded':downloaded,
            'left':self.torrent.torrent_size - downloaded,
            'compact':1
        }
        if first:
            params['first'] = 'started'

        url = self.torrent.announce +'?' + urlencode(params)
        logging.info('Connecting to tracker: {0}'.url)


        async with self.http_client.get(url) as response:
             if not response.status == 200:
                 raise ConnectionError('Unable to connect to the tracker:status code {}'.format(response.status))
             data = await response.read()
             self.raise_for_error(data)
             return TrackerResponse(bencoding.Decoder(data).decode())

    def close(self):
        self.http_client.close()

    def raise_for_error(self, tracker_response):
        """
        A (hacky) fix to detect errors by tracker even when the response has status code 200
        :param tracker_response:
        :return:
        """
        try:
            message = tracker_response.decode("utf-8")
            if "failure" in message:
                raise ConnectionError('Unable to connect to the tracker: {}'.format(message))

        except UnicodeDecodeError:
            pass

    def _construct_tracker_parameters(self):
        """
        Construct  the url parameters  used when issuing the announce call

        """

        return{
            'info_hash': self.torrent.info_hash,
            'peer_id': self.peer_id,
            'port': 6889,
            'uploaded':self.torrent.torrent_size,
            'downloaded':self.torrent.torrent_size,
            'left':self.torrent.torrent_size - self.torrent.torrent_size,
            'compact':1
        }

    def calculate_peer_id(self):

        return '-PC0001' +''.join(
            [str(random.randint(0, 9)) for _ in range(12)]
        )

    def decode_port(port):
        return unpack('>H', port)[0]



class TrackerResponse:

    def __init__(self, response:dict):
        self.response = response

    @property
    def failures(self):
        """
        Error message to be displayed in case of a failed response
        """
        if b'failure reason' in self.response:
            return self.response[b'failure reason'].decode('utf-8')
        return None

    @property
    def interval(self)-> int:
        """
        Interval in seconds that the client should wait for between sending requests to tracker
        """
        return self.response.get(b'interval',0)

    @property
    def completed(self)-> int:
       """
       Number of peers with the entire file ,i.e seeders
       """
       return self.response.get(b'completed',0)

    @property
    def incomplete(self)->int:
       """
      Number of non-seeders (leechers)
       """
       return self.response.get(b'incomplete',0);

    @property
    def peers(self):
        peers = self.response[b'peers']
        if type(peers) == list:
            logging.debug('Dictionary model peers are returned by the tracker')
            raise NotImplementedError()
        else:
            logging.debug('Binary model peers are returned by the tracker')


            peers = [peers[i:i+6] for i in range(0, len(peers), 6)]

            return [(socket.inet_ntoa(p[:4]),decode_port(p[4:])) for p in peers]


    def _str_(self):
        return "incomplete:{incomplete}\n"\
               "completed:{completed}\n" \
               "interval: {interval}\n" \
               "peers: {peers}\n".format(
                incomplete=self.incomplete,
                complete=self.complete,
                interval=self.interval,
                peers=", ".join([x for (x, _) in self.peers]))










