#!/bin/bash
# Set production mode
export PRODUCTION=true

# Build frontend
cd frontend && npm run build
cd ..

# Start both processes using Procfile's format
npm run start & gunicorn -k uvicorn.workers.UvicornWorker backend.app.main:app

# Keep the script running
wait 