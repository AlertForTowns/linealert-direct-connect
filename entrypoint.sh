#!/bin/bash

# Custom entrypoint script for Node-RED container

# Print the Node-RED version for debugging
echo "Starting Node-RED version: $(node-red --version)"

# Ensure that Node-RED has the correct directory structure
echo "Ensuring necessary directories are in place..."
mkdir -p /data
mkdir -p /data/.node-red

# Set ownership of the directories (in case of permission issues)
echo "Setting ownership for /data/.node-red directory..."
chown -R node-red:node-red /data /data/.node-red

# Add detailed logging for troubleshooting
echo "Entrypoint script executed at $(date)" >> /data/entrypoint.log
echo "Data directory structure set up successfully." >> /data/entrypoint.log

# Check for the presence of settings.js
if [ ! -f "/data/settings.js" ]; then
    echo "settings.js not found. Using default settings." >> /data/entrypoint.log
else
    echo "settings.js found. Using provided settings." >> /data/entrypoint.log
fi

# Check environment variables for debugging
echo "Environment Variables:" >> /data/entrypoint.log
echo "NODE_RED_SETTINGS: $NODE_RED_SETTINGS" >> /data/entrypoint.log

# Add a debug message if environment variable NODE_RED_SETTINGS is not set
if [ -z "$NODE_RED_SETTINGS" ]; then
    echo "Warning: NODE_RED_SETTINGS environment variable is not set." >> /data/entrypoint.log
else
    echo "NODE_RED_SETTINGS is set to: $NODE_RED_SETTINGS" >> /data/entrypoint.log
fi

# Allow any initial environment variable overrides
if [ -z "$NODE_RED_SETTINGS" ]; then
    export NODE_RED_SETTINGS="/data/settings.js"  # Default to local settings.js if not set
    echo "Using default settings.js located at /data/settings.js" >> /data/entrypoint.log
fi

# Check if the required node modules are installed, if not, install them
if [ ! -d "/data/.node-red/node_modules" ]; then
    echo "Node modules not found. Installing dependencies..." >> /data/entrypoint.log
    cd /data/.node-red
    npm install --no-optional
    echo "Node modules installation complete." >> /data/entrypoint.log
else
    echo "Node modules already installed. Skipping installation." >> /data/entrypoint.log
fi

# Start Node-RED with the appropriate entrypoint
echo "Starting Node-RED with the command: node-red" >> /data/entrypoint.log
exec node-red "$@"
