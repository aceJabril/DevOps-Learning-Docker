# Build stage
FROM python:3.13-alpine AS build

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.13-alpine

WORKDIR /app

COPY --from=build /usr/local/lib/python3.13/site-packages \
                  /usr/local/lib/python3.13/site-packages

COPY app.py .

RUN adduser -D appuser
USER appuser

CMD ["python", "app.py"]