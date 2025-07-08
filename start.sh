#!/usr/bin/env bash

# Install Chrome
apt-get update && apt-get install -y wget gnupg unzip curl

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb

# Start the app
gunicorn app:app --bind 0.0.0.0:$PORT
