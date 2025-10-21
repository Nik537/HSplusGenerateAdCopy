"""
Cloud Run / Google Cloud Functions entry point
This is a wrapper for app.py to work with serverless platforms
"""
from app import app

# For Google Cloud Run
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
