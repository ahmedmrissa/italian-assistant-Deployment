# Use Python 3.9 slim image
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements-supabase.txt ./

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir websockets==9.1
RUN pip install --no-cache-dir sanic==21.9.0
RUN pip install --no-cache-dir rasa-sdk==3.6.2
RUN pip install --no-cache-dir --no-deps rasa==3.6.21
RUN pip install --no-cache-dir -r requirements-supabase.txt
RUN pip install --no-cache-dir aiohttp==3.8.1

COPY . .

# Render will inject $PORT — use it for Rasa HTTP API
EXPOSE 8080

# Start both Rasa server & action server
CMD sh -c "rasa train && \
           rasa run --enable-api --cors '*' --port ${PORT:-8080} --host 0.0.0.0 --debug & \
           rasa run actions --port 5055 --host 0.0.0.0 & \
           wait"
