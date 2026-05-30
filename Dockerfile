FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel \
    && for i in 1 2 3 4 5; do \
         pip install --no-cache-dir -r requirements.txt && break; \
         echo "pip install failed, retry $i/5..."; \
         sleep 15; \
       done

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "pinkshop.asgi:application"]
