#!/usr/bin/env python3
"""Development server with auto-rebuild on file changes."""

import http.server
import socketserver
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from build import build

PORT = 1313
BASE_DIR = Path(__file__).parent
PUBLIC_DIR = BASE_DIR / "public"


class RebuildHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_build = 0

    def on_any_event(self, event):
        if event.is_directory:
            return
        if "__pycache__" in str(event.src_path):
            return
        now = time.time()
        if now - self.last_build > 1:
            self.last_build = now
            print(f"\n  Changed: {event.src_path}")
            try:
                build()
                print(f"  Serving at http://localhost:{PORT}\n")
            except Exception as e:
                print(f"  Build error: {e}\n")


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def log_message(self, format, *args):
        pass  # Suppress request logs


def serve():
    # Initial build
    print("Building site...")
    build()

    # Setup file watcher
    handler = RebuildHandler()
    observer = Observer()
    for watch_dir in ["content", "templates", "data", "static", "admin"]:
        path = BASE_DIR / watch_dir
        if path.exists():
            observer.schedule(handler, str(path), recursive=True)
    observer.start()

    # Start HTTP server
    with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
        httpd.allow_reuse_address = True
        print(f"\n  Serving at http://localhost:{PORT}")
        print(f"  Admin panel at http://localhost:{PORT}/admin/")
        print("  Watching for changes... (Ctrl+C to stop)\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            observer.stop()
    observer.join()


if __name__ == "__main__":
    serve()
