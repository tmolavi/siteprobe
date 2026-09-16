import http.server
import socketserver
import threading
from pathlib import Path
import pytest


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "test_site"


class CustomMockHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FIXTURES_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/redirect-1":
            self.send_response(301)
            self.send_header("Location", "/redirect-2")
            self.end_headers()
            return
        elif self.path == "/redirect-2":
            self.send_response(302)
            self.send_header("Location", "/destination.html")
            self.end_headers()
            return
        elif self.path == "/broken.html":
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 Not Found</h1>")
            return
        elif self.path == "/robots.txt":
            # Test site intentionally has no robots.txt initially
            self.send_response(404)
            self.end_headers()
            return
        super().do_GET()

    def log_message(self, format, *args):
        # Suppress noisy mock server logs during test runs
        pass


@pytest.fixture(scope="session")
def mock_server():
    port = 8899
    handler = CustomMockHandler
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        yield f"http://127.0.0.1:{port}"
        httpd.shutdown()
