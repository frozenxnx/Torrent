# BitTorrent Client (Python)

A lightweight BitTorrent client implemented from scratch in Python using async I/O, custom bencoding/decoding, and tracker communication.  
This project demonstrates deep understanding of peer-to-peer networking, socket programming, and the BitTorrent protocol.

## 🚀 Features

- **Torrent File Parser** – Decodes `.torrent` files and extracts metadata like announce, info_hash, and file size.  
- **Tracker Communication** – Sends HTTP(S) announce requests to trackers and parses peer responses.  
- **Peer ID Generation** – Implements the official 20-byte peer identification mechanism.  
- **Bencoding Implementation** – Custom encoder/decoder for BitTorrent’s data serialization format.  
- **Async HTTP Requests** – Uses `aiohttp` for non-blocking tracker connections.  
- **Structured Testing** – Unit tests for Tracker responses, peer ID generation, and failure handling.  

## 🧩 Tech Stack

| Component           | Technology            |
|---------------------|-----------------------|
| Language            | Python 3.10+          |
| Networking          | aiohttp, socket       |
| Data Serialization  | Custom bencoding module |
| Testing             | unittest              |
| Logging             | Python logging module |

## 🧠 Key Modules

- `pieces/Tracker.py` – Handles tracker requests and peer list parsing.  
- `pieces/Torrent.py` – Manages torrent metadata and info hash extraction.  
- `pieces/bencoding.py` – Encodes/decodes tracker communication data.  
- `pieces/client.py` – Coordinates the Torrent and Tracker classes.  
- `test/TrackerTest.py` – Contains tracker-related unit tests.

## ⚙️ Installation

git clone https://github.com/your-username/bittorrent-client.git
cd bittorrent-client
pip install -r requirements.txt


## ▶️ Usage

python main.py <path_to_torrent_file>


Example:

python main.py ubuntu-22.04.torrent


## 🧪 Running Tests

python -m unittest discover tests



## 🔍 Highlights

- Implemented BitTorrent tracker communication logic without external libraries.  
- Demonstrated async programming via aiohttp for concurrent network calls.  
- Built modular, testable architecture — each core component is independently verifiable.  
- Developed custom binary parsers for peer list and port decoding.

## 💡 Future Enhancements

- Peer handshake and block exchange.  
- Download management (piece selection, reassembly).  
- Upload capability for seeding.  
- Web-based frontend to visualize download progress.


