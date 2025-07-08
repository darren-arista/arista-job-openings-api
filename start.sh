#!/usr/bin/env bash

# Ensure dependencies and Chrome are installed
apt-get update
apt-get install -y wget gnupg2 curl unzip

# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb

# Start your Flask app
gunicorn app:app --bind 0.0.0.0:$PORT
