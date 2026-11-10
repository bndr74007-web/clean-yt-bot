FROM python:3.10
RUN apt-get update && apt-get install -y chromium chromium-driver
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "watch_bot.py"]
