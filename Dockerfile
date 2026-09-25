FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir "pytest>=8"
CMD ["python","rag_platform.py","architecture"]
