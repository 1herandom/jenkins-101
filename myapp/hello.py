from flask import Flask, jsonify
import signal
import sys

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Hello from myapp!</h1><p>Running and serving traffic.</p>"


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


def shutdown(signum, frame):
    print("SIGTERM received, shutting down...", flush=True)
    sys.exit(0)


signal.signal(signal.SIGTERM, shutdown)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
