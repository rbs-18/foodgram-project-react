FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY foodgram_project/ .

CMD ["gunicorn", "foodgram_project.wsgi:application", "--bind", "0:8000"]
