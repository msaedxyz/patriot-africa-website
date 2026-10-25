#!/usr/bin/env python3
"""Preview the Patriot Africa site on this computer.

  python3 preview.py              opens http://localhost:8000 on this Mac only
  python3 preview.py 8001         uses another port
  python3 preview.py --lan        also opens the preview to phones on the same Wi-Fi

Press Control+C to stop it.
"""
import http.server, os, socket, socketserver, sys, threading, webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "site")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
LAN = "--lan" in sys.argv
PORT = int(ARGS[0]) if ARGS else 8000


class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    """Serves /services from services.html, as Cloudflare Pages does."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE, **kwargs)

    def send_head(self):
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        local = os.path.join(SITE, path.lstrip("/"))
        if path not in ("", "/") and not os.path.splitext(path)[1] and os.path.isfile(local.rstrip("/") + ".html"):
            self.path = path.rstrip("/") + ".html" + self.path[len(path):]
        elif path != "/" and not os.path.exists(local):
            self.path = "/404.html"
        return super().send_head()

    def do_POST(self):
        self.send_response(501)
        self.end_headers()

    def log_message(self, fmt, *args):
        pass


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True


def lan_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return None


if __name__ == "__main__":
    if not os.path.isdir(SITE):
        sys.exit("Cannot find the 'site' folder next to preview.py. Run: python3 build.py")
    try:
        httpd = Server(("0.0.0.0" if LAN else "127.0.0.1", PORT), CleanURLHandler)
    except OSError:
        sys.exit("Port %d is busy. Run: python3 preview.py %d" % (PORT, PORT + 1))
    url = "http://localhost:%d" % PORT
    print("Patriot Africa preview is running at " + url)
    if LAN:
        ip = lan_address()
        if ip:
            print("On a phone on the same Wi-Fi, open http://%s:%d" % (ip, PORT))
    print("Press Control+C to stop it.")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
