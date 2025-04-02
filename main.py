from flask import send_from_directory, send_file
import os
import logging
from app import app

# Set up logging to see what's happening
logging.basicConfig(level=logging.DEBUG)

# Import routes to register them with Flask
# We don't need to import routes here because it's already imported in app.py

# Serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    logging.info(f"Serving static file: {path}")
    return send_from_directory('static', path)

# Serve the main HTML page for non-API routes
@app.route('/')
def index():
    logging.info("Serving index.html")
    return send_file('static/index.html')

# Catch-all route for SPA (Single Page Application) style routing
@app.route('/<path:path>')
def serve(path):
    # Skip API routes that are already defined in routes.py
    if path == 'health' or path == 'leads' or path.startswith('leads/') or path.startswith('notes/'):
        logging.info(f"Skipping API route: {path}")
        return
    
    # Serve static files if they exist
    if os.path.exists(f"static/{path}"):
        logging.info(f"Serving static file from catch-all: {path}")
        return send_from_directory('static', path)
    
    # Default to serving index.html for all other routes (SPA style)
    logging.info(f"Serving index.html for path: {path}")
    return send_file('static/index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
