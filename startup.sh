#!/bin/sh
# Simple startup script for Azure Web App (Linux)
# Azure's App Service will set $PORT; default to 8000 if not set.
exec gunicorn --bind 0.0.0.0:${PORT:-8000} app:app
