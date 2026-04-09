FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir gunicorn==20.1.0

COPY . .
COPY data/ingredients.csv /app/data/ingredients.csv

RUN mkdir -p /app/static /app/media

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi"]