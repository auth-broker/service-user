FROM python:3.12.7-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Configure ENV
ENV PYTHONBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Directory for package
WORKDIR /package

# Install project dependencies (ensures cache before project change)
COPY pyproject.toml tox.ini README.md .

# Inject a temporary .netrc from a build secret and run uv
RUN uv sync --no-install-project

# Install remaining project
COPY src ./src
COPY tests ./tests
RUN uv sync

# Default entrypoint for running FastAPI services
ENTRYPOINT ["uv", "run", "uvicorn"]
CMD ["ab_service.user.main:app", "--host", "0.0.0.0", "--port", "80"]
