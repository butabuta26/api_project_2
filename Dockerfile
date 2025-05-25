FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN mkdir -p static
RUN python manage.py collectstatic --noinput || echo 'collectstatic skipped'

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]















