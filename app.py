import os
import sys

# Ensure UTF-8 output encoding on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import json
import socket
import tempfile
import threading
import webbrowser
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Preload MarkItDown
try:
    from markitdown import MarkItDown
    print("[INFO] Initializing MarkItDown engine...")
    md_engine = MarkItDown()
    print("[INFO] MarkItDown engine ready!")
except Exception as e:
    print(f"[ERROR] Failed to initialize MarkItDown: {e}")
    md_engine = None

BASE_DIR = Path(__file__).resolve().parent
INDEX_HTML = BASE_DIR / "index.html"


class MarkItDownHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Custom concise logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

    def _send_json(self, status_code: int, data: dict):
        response_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Filename, X-Enable-Thai-OCR, X-Force-OCR")
        self.end_headers()

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path).path
        if parsed_path in ("/", "/index.html"):
            if not INDEX_HTML.exists():
                self.send_error(404, "index.html not found")
                return

            try:
                content = INDEX_HTML.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, f"Error reading index.html: {e}")
        else:
            self.send_error(404, "Path not found")

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path).path
        if parsed_path == "/api/convert":
            if md_engine is None:
                self._send_json(500, {
                    "success": False,
                    "error": "MarkItDown engine is not initialized. Please check server logs."
                })
                return

            try:
                # Get Content-Length
                content_length_header = self.headers.get("Content-Length")
                if not content_length_header:
                    self._send_json(400, {
                        "success": False,
                        "error": "Missing Content-Length header"
                    })
                    return

                content_length = int(content_length_header)
                if content_length <= 0:
                    self._send_json(400, {
                        "success": False,
                        "error": "Uploaded file is empty"
                    })
                    return

                # Read OCR configuration headers
                enable_thai_ocr = self.headers.get("X-Enable-Thai-OCR", "true").lower() in ("true", "1", "yes")
                force_ocr = self.headers.get("X-Force-OCR", "false").lower() in ("true", "1", "yes")

                # Get filename from X-Filename header
                encoded_filename = self.headers.get("X-Filename", "document.bin")
                filename = urllib.parse.unquote(encoded_filename)
                
                # Extract extension
                _, ext = os.path.splitext(filename)
                ext = ext.lower() if ext else ".bin"

                # Write incoming bytes to a temporary file with matching extension
                with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp_file:
                    temp_path = tmp_file.name
                    remaining = content_length
                    chunk_size = 64 * 1024  # 64 KB chunks
                    while remaining > 0:
                        read_bytes = self.rfile.read(min(remaining, chunk_size))
                        if not read_bytes:
                            break
                        tmp_file.write(read_bytes)
                        remaining -= len(read_bytes)

                # Process conversion with Thai OCR enhancement
                try:
                    image_extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}
                    markdown_text = ""
                    title = filename

                    if ext in image_extensions:
                        if enable_thai_ocr:
                            print(f"[INFO] Running Thai OCR on image: {filename}")
                            import thai_ocr
                            markdown_text = thai_ocr.ocr_image(temp_path)
                            if not markdown_text:
                                markdown_text = "*(ไม่พบข้อความจากการทำ OCR ในรูปภาพนี้)*"
                        else:
                            result = md_engine.convert(temp_path)
                            markdown_text = result.text_content or ""
                            title = result.title or filename
                    elif ext == ".pdf" and enable_thai_ocr:
                        import thai_ocr
                        mode_str = "Force OCR" if force_ocr else "Smart Hybrid (Digital + PUA + OCR Fallback)"
                        print(f"[INFO] Processing PDF [{mode_str}]: {filename}")
                        markdown_text = thai_ocr.ocr_pdf(temp_path, force_ocr=force_ocr)
                    else:
                        # Standard MarkItDown conversion for Office / Text files
                        result = md_engine.convert(temp_path)
                        markdown_text = result.text_content or ""
                        title = result.title or filename

                    self._send_json(200, {
                        "success": True,
                        "filename": filename,
                        "title": title,
                        "markdown": markdown_text
                    })
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_path):
                        try:
                            os.remove(temp_path)
                        except OSError:
                            pass

            except Exception as e:
                print(f"[ERROR] Conversion failed: {e}")
                self._send_json(500, {
                    "success": False,
                    "error": f"การแปลงไฟล์ล้มเหลว: {str(e)}"
                })
        else:
            self.send_error(404, "Endpoint not found")


def find_free_port(start_port: int = 8080) -> int:
    port = start_port
    while port < 65535:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
            port += 1
    return start_port


def main():
    import argparse
    parser = argparse.ArgumentParser(description="MarkItDown Web UI Server")
    parser.add_argument("--port", type=int, default=None, help="Port to listen on (default: 8080 or next free port)")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open the web browser")
    args = parser.parse_args()

    port = args.port if args.port else find_free_port(8080)
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, MarkItDownHandler)

    url = f"http://127.0.0.1:{port}"
    print("=" * 60)
    print(" [*] MarkItDown Web UI Server พร้อมใช้งานแล้ว!")
    print(f" [*] กรุณาเปิดเบราว์เซอร์ที่: {url}")
    print(" [*] กด Ctrl+C ในหน้าต่างนี้เพื่อหยุดการทำงาน")
    print("=" * 60)

    if not args.no_browser:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Stopping server...")
    finally:
        httpd.server_close()
        print("[INFO] Server stopped.")


if __name__ == "__main__":
    main()
