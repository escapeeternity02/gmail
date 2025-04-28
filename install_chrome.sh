#!/bin/bash

# Download the headless Chrome binary (latest version compatible with Selenium)
echo "Downloading headless Chrome..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O google-chrome-stable_current_amd64.deb

# Extract the contents without needing sudo
echo "Extracting Chrome..."
mkdir -p /app/chrome
dpkg-deb -x google-chrome-stable_current_amd64.deb /app/chrome

# Set the binary location for Chrome
export GOOGLE_CHROME_BIN="/app/chrome/usr/bin/google-chrome-stable"
export CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)

# Download and install ChromeDriver
echo "Downloading ChromeDriver..."
wget https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip -P /app/
unzip /app/chromedriver_linux64.zip -d /app/

# Set the environment variables for the driver
export PATH=$PATH:/app/chromedriver

# Install Python dependencies
pip install -r requirements.txt

# Finish
echo "Chrome and Chromedriver installation complete!"
