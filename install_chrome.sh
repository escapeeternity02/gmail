#!/bin/bash

# Update package lists
sudo apt-get update

# Install dependencies
sudo apt-get install -y wget gnupg

# Install Google Chrome (headless)
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f  # To fix any dependency issues
