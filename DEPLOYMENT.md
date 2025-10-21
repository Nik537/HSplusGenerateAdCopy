# Firebase Deployment Guide

## Prerequisites

1. **Firebase CLI installed:**
   ```bash
   npm install -g firebase-tools
   ```

2. **Firebase account:** Create a project at https://console.firebase.google.com/

## Deployment Steps

### 1. Configure Firebase Project

```bash
# Login to Firebase
firebase login

# Initialize Firebase (if not already done)
firebase init hosting

# Select your project or create a new one
# Choose 'frontend/dist' as the public directory
# Configure as single-page app: Yes
# Don't overwrite index.html
```

### 2. Update API Endpoint

Since Firebase only hosts static files, you'll need to deploy the backend separately. Options:

**Option A: Use Firebase Functions (Recommended)**
- Convert Flask app to Firebase Cloud Functions
- Requires refactoring backend code

**Option B: Deploy Backend to Cloud Run / Heroku / Railway**
- Keep backend as-is
- Update frontend API URL to point to deployed backend

**Option C: Use Vercel/Netlify for Full Stack**
- Deploy both frontend and backend together

### 3. Update Frontend API URL

Edit `frontend/src/utils/api.js`:

```javascript
// Change from localhost to your deployed backend URL
const API_BASE_URL = 'https://your-backend-url.com';
```

### 4. Build Frontend

```bash
cd frontend
npm run build
```

This creates optimized production files in `frontend/dist/`

### 5. Deploy to Firebase

```bash
# From project root
firebase deploy --only hosting
```

### 6. Configure Environment Variables

Your backend needs to be deployed with:
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`

**For Firebase Functions:**
```bash
firebase functions:config:set anthropic.key="YOUR_KEY"
firebase functions:config:set openai.key="YOUR_KEY"
```

**For other platforms:** Use their environment variable configuration

## Backend Deployment Options

### Option 1: Google Cloud Run (Recommended for Firebase)

1. **Install Google Cloud CLI**
2. **Build and deploy:**
   ```bash
   cd backend
   gcloud run deploy marketing-copy-api \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars ANTHROPIC_API_KEY=xxx,OPENAI_API_KEY=xxx
   ```

### Option 2: Heroku

```bash
# From backend directory
heroku create marketing-copy-api
heroku config:set ANTHROPIC_API_KEY=xxx
heroku config:set OPENAI_API_KEY=xxx
git push heroku main
```

### Option 3: Railway.app

1. Connect GitHub repo
2. Select backend folder
3. Add environment variables in dashboard
4. Auto-deploy on push

### Option 4: Vercel (Full Stack)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy entire project
vercel

# Add environment variables in Vercel dashboard
```

## Post-Deployment

1. **Update CORS settings** in backend to allow your Firebase domain:
   ```python
   CORS(app, origins=['https://your-app.web.app'])
   ```

2. **Test all features:**
   - URL scraping
   - Copy generation with all AI models
   - Export functionality

3. **Set up monitoring:**
   - Firebase Analytics
   - Backend error logging

## Security Checklist

- [ ] API keys stored as environment variables (never in code)
- [ ] CORS properly configured
- [ ] Rate limiting enabled on backend
- [ ] Firebase security rules configured
- [ ] HTTPS enforced

## Custom Domain (Optional)

1. In Firebase Console → Hosting → Add custom domain
2. Follow DNS configuration steps
3. SSL certificate auto-provisioned

## Useful Commands

```bash
# View live site
firebase open hosting:site

# View deployment history
firebase hosting:channel:list

# Deploy to preview channel (for testing)
firebase hosting:channel:deploy preview

# View logs
firebase functions:log
```

## Troubleshooting

**Build fails:**
- Check Node version (v18+ recommended)
- Clear node_modules and reinstall

**API calls fail:**
- Verify backend URL in frontend
- Check CORS configuration
- Ensure environment variables are set

**Scraping doesn't work:**
- May need to enable CORS proxy
- Or deploy backend with same origin

## Support

For issues, check:
- Firebase documentation: https://firebase.google.com/docs/hosting
- Backend deployment guides for your chosen platform
