FROM python:3.11-slim AS base

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

RUN python -m allosaurus.bin.download_model -m eng2102

COPY ./resources /code/resources

# ---------------------
# Test stage
# ---------------------
FROM base AS test

COPY ./tests /code/tests

CMD ["pytest"]

# ---------------------
# Development stage
# ---------------------
FROM base AS dev

CMD ["fastapi", "run", "app/main.py", "--port", "8001"]

# ---------------------
# Production stage
# ---------------------
FROM base AS prod

CMD ["fastapi", "run", "app/main.py", "--port", "8001", "--workers", "4"]