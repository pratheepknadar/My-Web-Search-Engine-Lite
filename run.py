# main.py
from src.downloader import CommonCrawlDownloader
from src.indexer import SearchIndexer

def run_indexing_pipeline(limit=500):
    downloader = CommonCrawlDownloader()
    indexer = SearchIndexer()
    
    # Use this updated path (CC-MAIN-2024-10 is a good recent crawl)
    # Use this path instead - it is much lighter!
    sample_path = "crawl-data/CC-MAIN-2024-10/segments/1707947473347.0/wet/CC-MAIN-20240220211055-20240221001055-00000.warc.wet.gz"
    
    count = 0
    buffer = []
    
    print("Connecting to Common Crawl...")
    
    # DEBUG: Check if the stream even starts
    for i, data in enumerate(downloader.stream_records(sample_path)):
        # HEARTBEAT: Print this to see if any data is arriving
        print(f"Checking record {i}...", end="\r") 
        
        url = data.get('url')
        text = data.get('text', '')
        
        if url and text:
            title = url.split('//')[-1].split('/')[0] 
            buffer.append((url, title, text))
            
            if len(buffer) >= 20:
                indexer.batch_add_to_index(buffer)
                print(f"\n[DB] Committed {len(buffer)} records to disk.")
                buffer = []

    if buffer:
        indexer.batch_add_to_index(buffer)
        
    if count == 0:
        print("❌ ERROR: No records were found. Check your internet or the file path.")
    else:
        print(f"✅ SUCCESS: Indexed {count} pages total.")

if __name__ == "__main__":
    run_indexing_pipeline(limit=5000) # Index 5,000 pages to start