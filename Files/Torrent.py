from hashlib import sha1
from collections import namedtuple

from . import bencoding

# Represent the files within torrent (i.e the files to write to disk)
TorrentFile = namedtuple('TorrentFile', ['name', 'size', 'hash'])

class Torrent:
    """
    Represent a torrent meta-data that is kept within .torrent file. It is basically just a
     wrapper around the bencoded data with utility function.

     This class does not contain any session state as part of the download
    """

    def __init__(self, filename):
        self.filename = filename
        self.files = []

        with open(self.filename, 'rb') as f:
            meta_info = f.read()
            self.meta_info = bencoding.Decoder(meta_info).decode()
            info = bencoding.Encoder(self.meta_info[b'info']).encode()
            self.info_hash = sha1(info).digest()
            self._identity_files()


    def  _identity_files(self):
        """
        Identify all files in the torrent file
        :return:
        """

        if self.multi_files:
            raise RuntimeError('Multi-files are not supported!')
        self.files.append(
            TorrentFile(
              self.meta_info[b'info'][b'name'].decode('utf-8'),
              self.meta_info[b'info'][b'length'],
              hash=None
        )
    )

    @property
    def announce(self)-> str:
        """
        The announce URL to the tracker
        :return:
        """
        return self.meta_info[b'announce'].decode('utf-8')

    @property
    def multi_files(self)-> bool:
        """
        Does this torrent  contain multiple files?
        :return:
        """
        # If the info dic containa a files element then it is a multi-file
        return b'files' in self.meta_info[b'info']

    @property
    def piece_length(self)-> int:
        """
        Get the piece length of the torrent in byte

        """
        return self.meta_info[b'info'][b'piece length']

    @property
    def total_size(self)->int:
        """
        The total size for all file in this torrent in bytes. for a single file torrent
        this is the only file , for a multi_file torrent this is the sum of all the files

       :return: the total size of the torrent in bytes
        """
        if self.multi_files:
            raise RuntimeError('Multi-files torrents are not supported!')
        return self.files[0].size


    @property
    def pieces(self):
        # The info pieces is a string representing all places SHA1 hashes
        # (each 20 bytes long). Read that data and slice it up  into the
        # actual peice
        data =  self.meta_info[b'info'][b'pieces']
        pieces =[]
        offset=0
        length = len(data)

        while offset < length:
            pieces.append(data[offset:offset + 20])
            offset +=20
        return pieces

    @property
    def output_file(self):
        return self.meta_info[b'info'][b'name'].decode('utf-8')

    def __str__(self):
        return 'Filename: {0}\n'\
               'File Length: {1}\n'\
               'Announce URL : {2n}\n'\
               'Hash:{3}'.format(self.meta_info[b'info'][b'name'],
                                 self.meta_info[b'info'][b'name'],
                                 self.meta_info[b'announce'],
                                 self.info_hash)










