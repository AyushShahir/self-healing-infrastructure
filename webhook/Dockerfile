FROM python:3.12-alpine

WORKDIR /app

RUN pip install --no-cache-dir flask==3.1.1

COPY app.py .

RUN mkdir -p /logs

EXPOSE 5000

CMD ["python", "app.py"]
