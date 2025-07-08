FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    chromium chromium-driver \
    curl unzip gnupg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
