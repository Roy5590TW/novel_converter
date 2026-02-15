# --- (Builder) ---
FROM python:3.10-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

# --- (Runtime) ---
FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY src/ ./src/
COPY static/ ./static/
COPY main.py ./

RUN mkdir -p inputs data && \
    chown -R 1000:1000 /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

USER 1000

EXPOSE 8080

CMD ["python", "main.py"]