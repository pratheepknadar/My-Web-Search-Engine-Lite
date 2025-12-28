from flask import Flask, render_template, request
from engine import SearchEngine # Import the logic wrote previously

app = Flask(__name__)
search_logic = SearchEngine()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    # Get the search term from the URL (e.g., /search?q=python)
    query = request.args.get('q', '')
    
    if query:
        # Call the engine.py search function
        results = search_logic.search(query, limit=15)
    else:
        results = []
        
    return render_template('index.html', query=query, results=results)

if __name__ == '__main__':
    # Run the local server
    print("Search engine running at http://127.0.0.1:5000")
    app.run(debug=True)