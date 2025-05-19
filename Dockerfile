FROM python:3.13-slim

WORKDIR /app

COPY . .
RUN pip install .

CMD ["uvicorn", "src.statusx.main:app", "--host", "0.0.0.0", "--port", "8000"]
