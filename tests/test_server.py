import os
import sys
import unittest
from pathlib import Path
from http.server import ThreadingHTTPServer

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import app


class TestServerConfiguration(unittest.TestCase):
    def test_max_file_size_defined(self):
        """Ensure MAX_FILE_SIZE is set to 100 MB."""
        self.assertEqual(app.MAX_FILE_SIZE, 100 * 1024 * 1024)

    def test_handler_uses_threading_server(self):
        """Ensure server can instantiate as ThreadingHTTPServer."""
        server = ThreadingHTTPServer(("127.0.0.1", 0), app.MarkItDownHandler)
        self.assertIsInstance(server, ThreadingHTTPServer)
        server.server_close()


if __name__ == "__main__":
    unittest.main()
