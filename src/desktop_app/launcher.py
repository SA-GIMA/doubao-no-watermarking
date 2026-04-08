from __future__ import annotations

import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path
from urllib.request import urlopen

import uvicorn

if __package__ in {None, ""}:
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from src.desktop_app.server import create_app
else:
    from .server import create_app

try:
    import webview
except ImportError:  # pragma: no cover - fallback for environments without pywebview
    webview = None


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_for_server(url: str, timeout: float = 20.0) -> None:
    deadline = time.time() + timeout
    last_error = None
    while time.time() < deadline:
        try:
            with urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return
        except Exception as exc:  # pragma: no cover - network timing differs per machine
            last_error = exc
            time.sleep(0.2)
    raise RuntimeError(f"Server did not become ready in time: {last_error}")


def main() -> None:
    port = _find_free_port()
    app = create_app()
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    base_url = f"http://127.0.0.1:{port}"
    _wait_for_server(f"{base_url}/health")

    try:
        if webview is not None:
            webview.create_window("doubao-no-watermarking", base_url, width=1180, height=860, min_size=(960, 720))
            webview.start()
        else:
            webbrowser.open(base_url)
            while thread.is_alive():
                time.sleep(0.5)
    finally:
        server.should_exit = True
        thread.join(timeout=5)


if __name__ == "__main__":
    main()
