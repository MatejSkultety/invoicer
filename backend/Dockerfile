# syntax=docker/dockerfile:1.7

############################################################
#  Args
############################################################
ARG PYTHON_VERSION=3.10.14-slim-bookworm

############################################################
#  Builder: install deps into a venv
############################################################
FROM python:${PYTHON_VERSION} AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /build
COPY backend/requirements.txt .

# Install dependencies using pip cache
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip setuptools wheel && \
    /opt/venv/bin/pip install \
      -i https://pypi.org/simple \
      --only-binary=:all: \
      --no-binary=pyperclip \
      -r requirements.txt

############################################################
#  Runtime
############################################################
FROM python:${PYTHON_VERSION} AS runtime

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -u 10001 appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Bring in the ready-to-run venv
COPY --from=builder /opt/venv /opt/venv

# Create app directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser backend/ /app/

# Switch to non-root user
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import sys, urllib.request; r=urllib.request.urlopen('http://localhost:8080/health', timeout=2); sys.exit(0 if 200<=r.status<300 else 1)"

# Run the application
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
