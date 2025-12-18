from flask import Flask, jsonify, request, render_template
from services import (
    dedup_service,
    staging_service,
    commit_service
)
from config import IMAGES
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template(
        "index.html",
        images=sorted(os.listdir(IMAGES))
    )

@app.route("/staging")
def staging():
    return jsonify(staging_service.get())

@app.route("/mark/<img>", methods=["POST"])
def mark(img):
    staging_service.mark(img)
    return "", 204

@app.route("/unmark/<img>", methods=["POST"])
def unmark(img):
    staging_service.unmark(img)
    return "", 204

@app.route("/dedup", methods=["POST"])
def dedup():
    return jsonify(dedup_service.run(request.json or {}))

@app.route("/commit", methods=["POST"])
def commit():
    r = commit_service.commit()
    return jsonify(r) if r else ("empty", 400)

@app.route("/history")
def history():
    return jsonify(commit_service.history())

@app.route("/rollback/<int:cid>", methods=["POST"])
def rollback(cid):
    return ("", 204) if commit_service.rollback(cid) else ("not found", 404)

if __name__ == "__main__":
    app.run(debug=True)
