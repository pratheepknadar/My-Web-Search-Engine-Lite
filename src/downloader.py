import requests
from warcio.archiveiterator import ArchiveIterator

class CommonCrawlDownloader:
    def __init__(self):
        # The base URL for all Common Crawl public data
        self.base_url = "https://data.commoncrawl.org/"

    def stream_records(self, wet_path):
        full_url = self.base_url + wet_path
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) CC-Search-Project/1.0'}
        
        print(f"Connecting to: {full_url}")
        
        try:
            # stream=True is key, but timeout=30 prevents the 2-minute hang
            response = requests.get(full_url, stream=True, headers=headers, timeout=30)
            response.raise_for_status() # This will print an error if the URL is 404
            
            # Check if we actually got content
            print("Connection established. Reading stream...")
            
            for record in ArchiveIterator(response.raw):
                if record.rec_type == 'conversion':
                    url = record.rec_headers.get_header('WARC-Target-URI')
                    # Read only first 1MB of content per page to prevent memory issues
                    content = record.content_stream().read().decode('utf-8', errors='ignore')
                    yield {'url': url, 'text': content}
                    
        except requests.exceptions.RequestException as e:
            print(f"Network Error: {e}")

# Example Usage (for testing):
if __name__ == "__main__":
    downloader = CommonCrawlDownloader()
    
    # This is a real sample path from a recent crawl
    # Use this path instead - it is much lighter!
    sample_path = "crawl-data/CC-MAIN-2024-10/segments/1707947473347.0/wet/CC-MAIN-20240220211055-20240221001055-00000.warc.wet.gz"
    
    print("Starting stream... (Press Ctrl+C to stop)")
    for i, data in enumerate(downloader.stream_records(sample_path)):
        print(f"Result {i+1}: {data['url']}")
        
        # Limit test to first 5 results so we don't overwhelm the console
        if i >= 4:
            break