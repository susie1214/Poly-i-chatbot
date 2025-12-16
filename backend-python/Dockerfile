FROM python:3.11-slim
WORKDIR /app

# system deps for building some Python packages (llama-cpp-python may need cmake/build tools)
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential cmake git libgomp1 libopenblas-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1
EXPOSE 5001
CMD ["python", "app.py"]
