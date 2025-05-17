# to start  the backend run Port 8000 (http://127.0.0.1:8000):
cd backend
python -m uvicorn app.main:app --reload

# to start the frontend (dev server) Port 3000 (http://localhost:3000):
Make sure you're in the root directory (where package.json is)
cd frontend
npm run dev

# Heroku Deployment
This application is configured for Heroku deployment with both Python backend and Next.js frontend.

## Deploying to Heroku
1. Install the Heroku CLI
2. Login to Heroku: `heroku login`
3. Create a new Heroku app (if not already created): `heroku create your-app-name`
4. Set your app to use both buildpacks:
   ```
   heroku buildpacks:clear
   heroku buildpacks:add heroku/nodejs
   heroku buildpacks:add heroku/python
   ```
5. Set remote repository: `heroku git:remote -a your-app-name`
6. Set environment variables:
   ```
   heroku config:set PRODUCTION=true
   heroku config:set DATA_PATH=/path/to/data/file.xlsx
   ```
7. Push to Heroku: `git push heroku main`

## Environment Variables
- `PRODUCTION`: Set to "true" for production mode (serves frontend files)
- `DATA_PATH`: Path to your Excel data file on Heroku (optional)

## Data Storage
Since Heroku has an ephemeral filesystem, consider using:
- Heroku Postgres for database storage instead of Excel files
- AWS S3 or similar for persistent file storage



