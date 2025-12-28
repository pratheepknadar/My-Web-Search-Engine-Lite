# My-Web-Search-Engine-Lite: A Python-Powered Web Search Engine

A functional, local search engine built using Python and the Common Crawl public dataset. This project streams web data at scale, indexes it using a high-performance Full-Text Search (FTS) engine, and provides a Google-style web interface for querying.
![](https://github.com/pratheepknadar/My-Web-Search-Engine-Lite/blob/main/search%20engine.png)
## 🚀 Features
- **Zero-Cost Infrastructure:** Streams data directly from the Common Crawl Public HTTP gateway (no AWS account required).
- **Efficient Indexing:** Uses SQLite FTS5 with BM25 ranking for industry-standard search relevancy.
- **Memory Efficient:** Processes multi-gigabyte files using Python generators and stream-processing to maintain a low RAM footprint.
- **Instant Snippets:** Generates highlighted search previews (snippets) showing query matches in context.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Data Source:** Common Crawl (WET datasets)
- **Database:** SQLite (FTS5 Extension)
- **Web Framework:** Flask
- **Libraries:** Warcio, Requests

## 📂 Architecture
1. **Downloader:** Connects to the CC Public Repository and streams compressed WARC/WET records.
2. **Indexer:** Parses raw text and builds a local inverted index.
3. **Search Engine:** Executes keyword matching and relevancy ranking.
4. **Web UI:** A clean Flask-based front-end for user interaction.

## 🛠 Project Structure Explained
run.py: The entry point. It triggers the downloader and feeds data into the indexer.

src/downloader.py: Handles the HTTP stream from Common Crawl.

src/indexer.py: Creates the SQLite FTS5 tables and saves the text.

src/engine.py: Contains the logic for BM25 ranking and keyword matching.

src/web_ui.py: The Flask application that renders the search bar.
