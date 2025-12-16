# Stage 1: Build Frontend
FROM node:22-alpine as frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
# Ensure public assets (audio) are included in build
RUN npm run build

# Stage 2: Backend Runtime
FROM python:3.10-slim
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend from Stage 1
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# Expose port (Render will use $PORT environment variable, default 8000)
ENV PORT=8000
EXPOSE 8000

# Run the application
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port $PORT"]
