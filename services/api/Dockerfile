FROM python:3.12-slim
WORKDIR /workspace
COPY services/api/requirements*.txt services/api/constraints-python312.txt /workspace/services/api/
RUN pip install --no-cache-dir -r /workspace/services/api/requirements-lock.txt
COPY services/api/app /workspace/services/api/app
COPY apps/preview /workspace/apps/preview
COPY data/fixtures /workspace/data/fixtures
COPY benchmarks /workspace/benchmarks
RUN mkdir -p /workspace/runtime/uploads
WORKDIR /workspace/services/api
ENV APP_ENV=production PRIVATE_UPLOAD_DIR=/workspace/runtime/uploads DATABASE_URL=sqlite:////workspace/runtime/borderproof.sqlite3
EXPOSE 8000
CMD ["sh","-c","exec python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
