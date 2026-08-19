from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/users")
def users():
    # Intentional lab behavior: exposes dummy sensitive data
    # for testing the Data Exposure detection module.
    return jsonify({
        "id": 1,
        "username": "admin",
        "email": "admin@test.com",
        "phone": "0987654321",
        "api_key": "LAB-API-KEY-1234567890",
    })


@app.route("/api/search")
def search():
    q = request.args.get("q", "")

    # Intentional lab behavior:
    # reflects user input and simulates a SQL error.
    if any(token in q.lower() for token in ("union", " or ", "syntax")):
        return "You have an error in your SQL syntax", 500

    return f"Search result for {q}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)