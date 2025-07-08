#!/usr/bin/env bash

# Update and install dependencies
apt-get update
apt-get install -y wget gnupg2 unzip curl

# Install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb

# Run your Flask app with gunicorn
gunicorn app:app --bind 0.0.0.0:$PORT
