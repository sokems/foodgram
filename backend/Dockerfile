FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip setuptools==65.5.1 wheel

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY data/ingredients.csv /app/data/ingredients.csv
RUN mkdir -p /app/static /app/media

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi"]