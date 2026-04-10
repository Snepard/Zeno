FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "celery -A celery_app.celery_app worker -l info -Q lecture,podcast,ppt,flashcards & python dispatcher.py"]
