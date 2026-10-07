from flask import Flask, jsonify
import signal
import sys
import socket

app = Flask(__name__)


@app.route("/")
def home():
    hostname = socket.gethostname()
    return f"""
    <html>
      <head><title>myapp</title></head>
      <body style="font-family: sans-serif; padding: 40px;">
        <h1>Hello from new-ch!</h1>
        <p>Running in container: <code>{hostname}</code></p>
        <p>Status: <span style="color: green;">healthy</span></p>
      </body>
    </html>
    """


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


def shutdown(signum, frame):
    print("SIGTERM received, shutting down gracefully...", flush=True)
    sys.exit(0)


signal.signal(signal.SIGTERM, shutdown)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
