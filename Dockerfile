# Multi-stage Docker build for Marketing Copy Generator
# Backend (Flask) + Frontend (React/Vite)

FROM python:3.11-slim as backend

WORKDIR /app/backend

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Install Node.js for frontend build
FROM node:18-alpine as frontend-build

WORKDIR /app/frontend

# Install frontend dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy frontend code and build
COPY frontend/ .
RUN npm run build

# Final stage - combine backend + built frontend
FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend
COPY backend/ ./backend/

# Copy built frontend
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# Copy environment template
COPY .env.example .

# Expose port
EXPOSE 5000

# Set working directory to backend
WORKDIR /app/backend

# Run the Flask app
CMD ["python", "app.py"]
