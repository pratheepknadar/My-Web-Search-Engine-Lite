import sqlite3

class SearchEngine:
    def __init__(self, db_path="database/search_index.db"):
        self.db_path = db_path

    def search(self, query_string, limit=10):
        """
        Queries the SQLite FTS5 table and returns ranked results.
        """
        results = []
        with sqlite3.connect(self.db_path) as conn:
            # This allows accessing columns by name like row['url']
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # FTS5 'MATCH' syntax is very powerful for search.
            # We use 'bm25(search_engine)' to rank results by relevancy.
            sql = """
                SELECT url, title, snippet(search_engine, 2, '<b>', '</b>', '...', 20) as snippet
                FROM search_engine 
                WHERE content MATCH ? 
                ORDER BY bm25(search_engine) 
                LIMIT ?
            """
            
            try:
                cursor.execute(sql, (query_string, limit))
                for row in cursor.fetchall():
                    results.append({
                        "url": row["url"],
                        "title": row["title"] if row["title"] else row["url"],
                        "snippet": row["snippet"]
                    })
            except sqlite3.OperationalError as e:
                print(f"Search error (likely formatting): {e}")
                
        return results

# Example Usage:
if __name__ == "__main__":
    engine = SearchEngine()
    user_query = "python programming" # Try a word  indexed
    
    print(f"Searching for: {user_query}")
    results = engine.search(user_query)
    
    for i, res in enumerate(results):
        print(f"\nResult {i+1}: {res['title']}")
        print(f"URL: {res['url']}")
        print(f"Preview: {res['snippet']}")