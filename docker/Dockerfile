FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/* \
    && git clone https://github.com/PUVHAM/Image_Retrieval.git Image_Retrieval \
    && pip3 install -r Image_Retrieval/requirements.txt

WORKDIR /app/Image_Retrieval

EXPOSE 8501

HEALTHCHECK CMD ["curl", "--fail", "http://localhost:8501/_stcore/health"]

ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
