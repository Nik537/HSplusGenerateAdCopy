# Single-stage build - backend only (frontend served separately via Firebase)
FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies with version check
COPY backend/requirements.txt ./backend/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r backend/requirements.txt && \
    pip list | grep anthropic

# Copy backend code
COPY backend/ ./backend/

# Expose port 5001 to match Railway's routing
EXPOSE 5001

# Set working directory to backend
WORKDIR /app/backend

# Run with gunicorn on port 5001
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-5001} --log-level info"]
