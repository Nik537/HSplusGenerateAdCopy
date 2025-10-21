# Quick Firebase Deployment Guide

## Step 1: Deploy Backend (Choose One Option)

### Option A: Railway.app (Easiest - Recommended)

1. Go to https://railway.app/
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repository
5. Click "Add variables" and add:
   - `ANTHROPIC_API_KEY` = your-anthropic-key
   - `OPENAI_API_KEY` = your-openai-key
6. In Settings → Set Root Directory to: `backend`
7. Railway will auto-deploy and give you a URL like: `https://xxx.railway.app`

### Option B: Render.com (Free Tier Available)

1. Go to https://render.com/
2. Click "New" → "Web Service"
3. Connect GitHub and select this repo
4. Settings:
   - **Name:** marketing-copy-api
   - **Root Directory:** backend
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
5. Add Environment Variables:
   - `ANTHROPIC_API_KEY`
   - `OPENAI_API_KEY`
6. Click "Create Web Service"
7. Get your URL: `https://marketing-copy-api.onrender.com`

### Option C: Google Cloud Run

```bash
cd backend

# Build and deploy
gcloud run deploy marketing-copy-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=xxx,OPENAI_API_KEY=xxx
```

## Step 2: Update Frontend API URL

Edit `frontend/src/utils/api.js`:

```javascript
const API_BASE_URL = 'https://your-backend-url.railway.app';  // or .onrender.com
```

## Step 3: Rebuild Frontend

```bash
cd frontend
npm run build
```

## Step 4: Deploy to Firebase

```bash
# Install Firebase CLI (if not installed)
npm install -g firebase-tools

# Login
firebase login

# Initialize (first time only)
firebase init hosting
# Choose:
# - Select existing project or create new
# - Public directory: frontend/dist
# - Single-page app: Yes
# - Don't overwrite index.html

# Deploy
firebase deploy
```

## Step 5: Update Backend CORS

Once you have your Firebase URL (e.g., `https://your-app.web.app`), update `backend/app.py`:

```python
# Change this line:
CORS(app)

# To this:
CORS(app, origins=[
    'http://localhost:3000',  # For local development
    'https://your-app.web.app',  # Your Firebase URL
    'https://your-app.firebaseapp.com'
])
```

Then redeploy your backend.

## Quick Commands

```bash
# Redeploy frontend only
cd frontend && npm run build && cd .. && firebase deploy

# View live site
firebase open hosting:site

# View logs
firebase hosting:channel:list
```

## Testing Checklist

- [ ] Backend API is live and responding
- [ ] Frontend loads on Firebase URL
- [ ] Can scrape vigoshop.si products
- [ ] Can generate copy with Claude models
- [ ] Can generate copy with OpenAI models
- [ ] Export functionality works
- [ ] No CORS errors in browser console

## Troubleshooting

**"API Disconnected" error:**
- Check backend URL in `frontend/src/utils/api.js`
- Verify backend is deployed and running
- Check CORS settings in backend

**Build errors:**
```bash
# Clear cache and rebuild
cd frontend
rm -rf node_modules dist
npm install
npm run build
```

**Backend errors:**
- Check logs on Railway/Render dashboard
- Verify environment variables are set
- Ensure all dependencies in requirements.txt

## Your Deployment URLs

After deployment, you'll have:
- **Frontend:** https://your-app.web.app
- **Backend:** https://your-app.railway.app (or .onrender.com)

Save these URLs for future reference!
