import http.server
import socketserver
import hashlib
import os
import time
from email.utils import formatdate, parsedate_to_datetime

PORT = 8000
FILENAME = "index.html"

class CachingHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        # Only serve "/" or "/index.html"
        if self.path != "/" and self.path != f"/{FILENAME}":
            self.send_error(404, "File not found")
            return

        try:
            with open(FILENAME, "rb") as f:
                content = f.read()
        except FileNotFoundError:
            self.send_error(404, "File not found")
            return

        # Generate ETag as MD5 hash of content
        etag = hashlib.md5(content).hexdigest()

        # Get file last modified time (float) and format to HTTP-date string
        last_modified_timestamp = os.path.getmtime(FILENAME)
        last_modified_str = formatdate(last_modified_timestamp, usegmt=True)

        # Debug info
        print(f"GET {self.path}")
        print(f"File size: {len(content)} bytes")
        print(f"ETag: {etag}")
        print(f"Last-Modified: {last_modified_str}")

        # Get conditional headers from client
        if_none_match = self.headers.get("If-None-Match")
        if_modified_since = self.headers.get("If-Modified-Since")

        not_modified = False

        # Check ETag first
        if if_none_match == etag:
            not_modified = True
            print("ETag matches If-None-Match: sending 304 Not Modified")

        # Check Last-Modified if ETag did not match
        elif if_modified_since:
            try:
                ims_datetime = parsedate_to_datetime(if_modified_since)
                # Convert both to integer seconds (truncate microseconds)
                file_mod_sec = int(last_modified_timestamp)
                ims_sec = int(ims_datetime.timestamp())

                if ims_sec >= file_mod_sec:
                    not_modified = True
                    print("Last-Modified <= If-Modified-Since: sending 304 Not Modified")

            except Exception as e:
                print("Error parsing If-Modified-Since header:", e)

        # Send 304 if not modified
        if not_modified:
            self.send_response(304)
            self.send_header("ETag", etag)
            self.send_header("Last-Modified", last_modified_str)
            self.end_headers()
            return

        # Otherwise send full content with headers
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("ETag", etag)
        self.send_header("Last-Modified", last_modified_str)
        self.end_headers()

        print("Sending file content...")
        self.wfile.write(content)
        print("Done sending.")

def run_server():
    with socketserver.TCPServer(("", PORT), CachingHTTPRequestHandler) as httpd:
        print(f"Serving HTTP caching demo at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
