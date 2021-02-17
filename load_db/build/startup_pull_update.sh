#!/bin/sh -e

# Add the crontab (via crontab -e or similar)
# @reboot /usr/local/bin/your-script.sh

# Repository
REPO_NAME=docker_tests
REPO_URL=https://github.com/newnativeabq/docker_tests.git
APP_DIR=load_db/src/app

# Enter home directory
cd ~/
git clone $REPO_URL

# Copy App Directory
if [ -d "/app"]; then
    sudo rm -R /app
fi
sudo mkdir /app
sudo cp -R $REPO_NAME/$APP_DIR/* /app/

# Cleanup
rm -R -f $REPO_NAME

