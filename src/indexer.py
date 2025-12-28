import sqlite3
import os 

class SearchIndexer:
    def __init__(self, db_path="database/search_index.db"):
        self.db_path = db_path
        
    
        # Get the folder name from the path (e.g., "database")
        folder = os.path.dirname(self.db_path)
        # Create the folder if it doesn't exist
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
      
            
        self._setup_database()

    def _setup_database(self):
        """Creates a Full-Text Search (FTS5) table for high-speed searching."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # FTS5 makes 'content' searchable by keywords very efficiently
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS search_engine USING fts5(
                    url,
                    title,
                    content
                )
            """)
            conn.commit()

    def add_to_index(self, url, title, content):
        """Inserts a single website record into the index."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO search_engine (url, title, content) VALUES (?, ?, ?)",
                (url, title, content)
            )
            conn.commit()

    def batch_add_to_index(self, records):
        """
        Inserts multiple records at once for much better performance.
        Input: List of tuples [(url, title, content), ...]
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany(
                "INSERT INTO search_engine (url, title, content) VALUES (?, ?, ?)",
                records
            )
            conn.commit()

# Example Usage (Connecting Downloader to Indexer):
if __name__ == "__main__":
    # This simulates how you would use them together
    indexer = SearchIndexer()
    
    # Dummy data for testing
    sample_data = [
        ("https://example.com", "Example Site", "This is a site about python programming and search engines."),
        ("https://python.org", "Python Official", "The official home of the Python programming language.")
    ]
    
    print("Indexing sample data...")
    indexer.batch_add_to_index(sample_data)
    print("Done! Your database is now searchable.")