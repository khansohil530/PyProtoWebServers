# === Stage 1: Build Environment ===
FROM python:3.10-slim AS build

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies in a virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt

# === Stage 2: Runtime Environment ===
FROM python:3.10-slim AS runtime

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

# Copy the virtual environment from the build stage
COPY --from=build /opt/venv /opt/venv

# Set working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Expose application port (change if needed)
EXPOSE 8888

# Default command to run the application (adjust as needed)
CMD ["python", "wsgiserver.py", "flaskapp:app"]
