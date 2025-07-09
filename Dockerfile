FROM python:3.10-slim

# Install dependencies for Chrome
RUN apt-get update && apt-get install -y \
    wget gnupg2 curl unzip fonts-liberation \
    libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
    libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 \
    libxrandr2 xdg-utils libu2f-udev --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install && \
    rm google-chrome-stable_current_amd64.deb

# Verify chrome install path
RUN which google-chrome

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app
WORKDIR /app

# Expose the app port
EXPOSE 10000

# Run the app using Python directly (not Gunicorn)
CMD ["python", "app.py"]
