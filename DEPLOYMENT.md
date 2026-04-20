# Deployment Guide

This project is now prepared for a simple split deployment:

- `backend/` -> Render
- `frontend/` -> Netlify
- `sql/` -> hosted MySQL database

## 1. Create a Hosted MySQL Database

Use any MySQL-compatible provider you like. Good options:

- Railway MySQL
- Aiven for MySQL
- TiDB Cloud
- PlanetScale compatible MySQL workflow if your SQL features fit it

Create a database named `restaurant_chain`, then import:

```bash
mysql -h <HOST> -P <PORT> -u <USER> -p < sql/schema.sql
mysql -h <HOST> -P <PORT> -u <USER> -p < sql/seed.sql
```

Save these values:

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

## 2. Deploy the Backend on Render

This repo includes [render.yaml](/c:/Users/shrey/OneDrive/Desktop/restaurant_project/render.yaml), so Render can detect the service settings.

### Steps

1. Push this project to GitHub.
2. In Render, click `New +` -> `Web Service`.
3. Connect your GitHub repo.
4. Render should detect:
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. Add environment variables:

```env
DB_HOST=your-db-host
DB_PORT=3306
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=restaurant_chain
CORS_ORIGINS=https://your-site.netlify.app
FLASK_DEBUG=false
```

6. Deploy.
7. After deploy, open:

```text
https://your-render-service.onrender.com/health
```

You should get a healthy JSON response.

## 3. Deploy the Frontend on Netlify

This repo includes [netlify.toml](/c:/Users/shrey/OneDrive/Desktop/restaurant_project/netlify.toml) so Netlify knows to publish the `frontend` folder.

Before deploying, update [frontend/config.js](/c:/Users/shrey/OneDrive/Desktop/restaurant_project/frontend/config.js) with your backend URL:

```js
window.APP_CONFIG = {
  apiBaseUrl: "https://your-render-service.onrender.com"
};
```

### Steps

1. Commit the updated `frontend/config.js`.
2. Push to GitHub.
3. In Netlify, choose `Add new site` -> `Import an existing project`.
4. Connect the same repo.
5. Netlify should use:
   - Publish directory: `frontend`
   - Build command: none
6. Deploy.

## 4. Update Backend CORS

After Netlify gives you the final frontend URL, make sure Render uses that exact URL in:

```env
CORS_ORIGINS=https://your-final-site.netlify.app
```

If you want to allow multiple origins, separate them with commas:

```env
CORS_ORIGINS=https://your-final-site.netlify.app,http://localhost:5500
```

Redeploy the backend after changing env vars.

## 5. Final Smoke Test

Check these in order:

1. Backend health:
   `https://your-render-service.onrender.com/health`
2. Frontend opens on Netlify.
3. Dashboard loads summary cards.
4. Branches and customers load.
5. Creating a branch or customer works.
6. No CORS errors appear in the browser console.

## Notes

- `backend/Procfile` is included for platform compatibility.
- `frontend/config.example.js` shows the production config format.
- `backend/.env` is ignored by git through [.gitignore](/c:/Users/shrey/OneDrive/Desktop/restaurant_project/.gitignore).
