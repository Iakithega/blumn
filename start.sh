#!/bin/bash
# Set production mode
export PRODUCTION=true

# Start FastAPI server which will handle both API and serve the already-exported Next.js static files
gunicorn -k uvicorn.workers.UvicornWorker backend.app.main:app 