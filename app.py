"""
RECLAIM AI - Main Application Server
Entry point for the Intelligent Lost Document Recovery Agent
"""
import os
import sys
from pathlib import Path
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS

from config import Config
from database.db import init_db
from api.recovery_routes import api_bp
from agent.gemini_client import is_gemini_available

def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", static_url_path="")
    CORS(app)
    
    # Ensure database is initialized
    init_db()
    
    # Register API blueprint
    app.register_blueprint(api_bp)
    
    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "RECLAIM AI — Intelligent Lost Document Recovery Agent",
            "tagline": "Lost a document? Reclaim your next step.",
            "hackathon": "Agentic AI Hackathon 2026 — Powered by Ziro.Digital",
            "ai_engine_status": "LIVE_GEMINI_AI" if is_gemini_available() else "DETERMINISTIC_FALLBACK_AI",
            "version": "1.0.0",
            "database": "sqlite_connected"
        }), 200

    # Frontend SPA entry point
    @app.route("/", methods=["GET"])
    def index():
        return send_from_directory(app.static_folder, "index.html")

    # Global Error Handlers
    @app.errorhandler(404)
    def not_found(e):
        if request.path.startswith("/api/"):
            return jsonify({"status": "error", "message": "API endpoint not found."}), 404
        # Serve index.html for client-side navigation
        return send_from_directory(app.static_folder, "index.html")

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({
            "status": "error",
            "message": "Internal server error. Safe fallback engaged.",
            "detail": str(e)
        }), 500

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1"]
    print(f"==================================================")
    print(f"  RECLAIM AI — Lost Document Recovery Agent")
    print(f"  Tagline: 'Lost a document? Reclaim your next step.'")
    print(f"  AI Mode: {'LIVE_GEMINI_AI' if is_gemini_available() else 'DETERMINISTIC_FALLBACK_AI'}")
    print(f"  Running on: http://127.0.0.1:{port}")
    print(f"==================================================")
    app.run(host="0.0.0.0", port=port, debug=debug)
