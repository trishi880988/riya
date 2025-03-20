FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 libfreetype6

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
