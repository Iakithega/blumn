#!/bin/bash
# Set production mode
export PRODUCTION=true

# Build frontend
cd frontend && npm run build
cd ..

# Start FastAPI server which will handle both API and serve the Next.js static files
gunicorn -k uvicorn.workers.UvicornWorker backend.app.main:app 