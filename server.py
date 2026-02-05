#!/usr/bin/env python3
"""
Simple HTTP server for local testing of the flash cards application.
Serves files from the 'public' directory on port 8000.
"""
import http.server
import socketserver
import os
import sys

PORT = 8000
DIRECTORY = "public"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # CORS headers for local testing
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def log_message(self, format, *args):
        # Custom log format
        sys.stdout.write("%s - - [%s] %s\n" %
                        (self.address_string(),
                         self.log_date_time_string(),
                         format % args))


if __name__ == "__main__":
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Check if public directory exists
    if not os.path.exists(DIRECTORY):
        print(f"❌ Error: '{DIRECTORY}' directory not found!")
        sys.exit(1)

    # Create server
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("=" * 60)
        print(f"🚀 Flash Cards Server Running")
        print("=" * 60)
        print(f"📁 Serving files from: {os.path.abspath(DIRECTORY)}")
        print(f"🌐 Open in browser: http://localhost:{PORT}/")
        print(f"")
        print(f"Press Ctrl+C to stop the server")
        print("=" * 60)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")
            sys.exit(0)
