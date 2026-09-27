FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY sample_projects ./sample_projects
COPY tests ./tests

WORKDIR /app/backend

EXPOSE 5000

CMD ["python", "app.py"]