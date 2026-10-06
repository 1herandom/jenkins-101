from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify(
        status="ok",
        message="myapp is running",
        service="myapp",
    )


@app.route("/health")
def health():
    # Keep this simple and fast — the pipeline hits it on every deploy.
    return jsonify(status="healthy"), 200


if __name__ == "__main__":
    # host="0.0.0.0" is REQUIRED for Docker port forwarding to reach the app.
    # If you bind to 127.0.0.1, curl from the host gets an empty reply (exit 52).
    app.run(host="0.0.0.0", port=8000)
