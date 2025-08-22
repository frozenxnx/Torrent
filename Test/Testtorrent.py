import os
import unittest

from Files.Torrent import Torrent


class UbuntuTorrentTests(unittest.TestCase):
    def setUp(self):
        # Get the directory where this test file is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the torrent file
        torrent_path = os.path.join(current_dir, 'Sample', 'ubuntu-25.04-desktop-amd64.iso.torrent')
        self.t = Torrent(torrent_path)
    def test_instantiate(self):
        self.assertIsNotNone(self.t)

    def test_is_single_file(self):
        self.assertFalse(self.t.multi_files)

    def test_announce(self):
        self.assertEqual(
            'https://torrent.ubuntu.com/announce', self.t.announce)

    def test_piece_length(self):
        self.assertEqual(
            262144, self.t.piece_length)

    def test_file(self):
        self.assertEqual(1, len(self.t.files))
        self.assertEqual(
            'ubuntu-25.04-desktop-amd64.iso', self.t.files[0].name)
        self.assertEqual(6278520832, self.t.files[0].size)

    def test_hash_value(self):
        # hexdigest of the SHA1 '4344503b7e797ebf31582327a5baae35b11bda01',
        self.assertEqual(
            b'\x8a\x19W\x7f\xb5\xf6\x90\x97\x0c\xa4:W\xff\x10\x11\xae "D\xb8',
            self.t.info_hash)

    def test_total_size(self):
        self.assertEqual(6278520832, self.t.total_size)

    def test_pieces(self):
        self.assertEqual(23951, len(self.t.pieces))


class SXSWTorrentTests(unittest.TestCase):
    """
    Tests for multi-file torrent (should raise RuntimeError)
    """

    def setUp(self):
        # Get the test directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path properly
        self.torrent_path = os.path.join(current_dir, 'Sample', 'SXSW_2016_Showcasing_Artists_Part1.torrent')

    def test_multi_file_not_supported(self):
        """Verify multi-file torrents raise RuntimeError"""
        if not os.path.exists(self.torrent_path):
            self.skipTest("Test torrent file not found")

        with self.assertRaises(RuntimeError):
            Torrent(self.torrent_path)
