# Restaurant Chain Management System

Full-stack project with:

- `backend/`: Flask REST API
- `frontend/`: static dashboard
- `sql/`: schema, seed data, and analytics queries

## Stack

- Backend: Python, Flask, MySQL
- Frontend: plain HTML, CSS, JavaScript
- Database: any hosted MySQL-compatible service
- Recommended deployment:
  - Backend: Render
  - Frontend: Netlify
  - Database: Railway MySQL, Aiven MySQL, TiDB Cloud, or another hosted MySQL provider

## Local Setup

### 1. Create the database

```bash
mysql -u root -p < sql/schema.sql
mysql -u root -p < sql/seed.sql
```

### 2. Run the backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
python app.py
```

The API runs on `http://localhost:5000`.

### 3. Run the frontend

Set `frontend/config.js` to your API URL. For local development it already points to:

```js
window.APP_CONFIG = {
  apiBaseUrl: "http://localhost:5000"
};
```

Then open `frontend/index.html` in a browser.

## Deployment

Detailed steps are in [DEPLOYMENT.md](/c:/Users/shrey/OneDrive/Desktop/restaurant_project/DEPLOYMENT.md).

## Required Backend Environment Variables

```env
DB_HOST=your-db-host
DB_PORT=3306
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=restaurant_chain
CORS_ORIGINS=https://your-frontend-site.netlify.app
FLASK_DEBUG=false
```

## Useful Backend Endpoints

- `GET /health`
- `GET /analytics/summary`
- `GET /branches`
- `GET /customers`
- `GET /orders`
- `GET /inventory/alerts`
