# Quick Start Guide - Marketing Copy Generator

## 🚀 5-Minute Setup

### 1. Install Dependencies
```bash
# Run automated setup
./setup.sh

# OR manually:
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
```

### 2. Configure API Key
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your key
# ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 3. Start Application
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 4. Open Browser
```
http://localhost:3000
```

---

## 📖 30-Second Demo

1. **Click** "Beauty Product" example button
2. **Click** "Generate Ad Copy"
3. **Wait** 5-8 seconds for AI generation
4. **See** 3 Facebook ad variants
5. **Click** "Copy" on your favorite
6. **Done!** Paste into Facebook Ads Manager

---

## 🎯 Key Features at a Glance

| Feature | Description | Benefit |
|---------|-------------|---------|
| **Auto-scraping** | Paste vigoshop.si URL → auto-fill | Save time |
| **3 Variants** | Pain point, Benefit, Social proof | A/B testing ready |
| **Market-specific** | SI, DE, IT, AT, HR, BA | Localized tone |
| **EU Shipping** | Mandatory in every variant | Beat Temu/AliExpress |
| **Engagement Score** | 0-100 rating | Predict performance |
| **Export** | Copy or download TXT | Easy workflow |

---

## 📁 Project Structure (Simplified)

```
marketing-copy-generator/
├── backend/              # Python Flask API
│   ├── app.py           # Main server
│   ├── scraper.py       # Web scraper
│   └── copy_generator.py # AI integration
├── frontend/            # React UI
│   └── src/
│       ├── App.jsx      # Main component
│       └── components/  # Form + Preview
├── examples.txt         # Sample outputs
├── README.md           # Full documentation
└── setup.sh            # Auto-setup script
```

---

## 🔧 Common Tasks

### Load an Example
1. Click "Beauty Product", "Electronics", or "Automotive"
2. Form auto-fills
3. Click "Generate Ad Copy"

### Use Custom Product
1. Paste vigoshop.si URL **OR** enter details manually
2. Select market (Slovenia, Germany, etc.)
3. Choose objective (Conversion, Awareness, Engagement)
4. Click "Generate Ad Copy"

### Export Copy
- **Copy to clipboard**: Click "📋 Copy" on any variant
- **Download file**: Click "⬇️ Download TXT" at top

### Check Setup
```bash
python test_setup.py
```

---

## 🐛 Troubleshooting

### "API not configured" error
```bash
# Create .env in backend folder
echo "ANTHROPIC_API_KEY=sk-ant-your-key" > backend/.env
# Restart backend: python app.py
```

### Scraping fails
- ✅ Verify URL is from vigoshop.si
- ✅ Try manually entering product details
- ✅ Check internet connection

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend won't start
```bash
cd backend
pip install -r requirements.txt
python app.py
```

---

## 📊 Understanding Outputs

### Variant Angles
- **Pain Point** (Variant 1): "Tired of X? Try Y!"
- **Benefit** (Variant 2): "Imagine life with Y..."
- **Social Proof** (Variant 3): "Join 10,000+ happy customers..."

### Engagement Score
- **80-100**: Excellent (ready to run)
- **60-79**: Good (minor tweaks)
- **<60**: Needs work (regenerate)

### Character Count
- **<125**: Perfect for mobile
- **125-150**: Good
- **>150**: Too long (will be truncated)

---

## 🎨 Customization Tips

### Market Selection
- **SI** (Slovenia): Casual, local trust
- **DE** (Germany): Professional, quality
- **IT** (Italy): Warm, family-oriented
- **AT** (Austria): Reliable, quality
- **HR** (Croatia): Friendly, casual
- **BA** (Bosnia): Straightforward, warm

### Ad Objective
- **Awareness**: Broader reach, curiosity
- **Conversion**: Direct sale, urgency
- **Engagement**: Likes/shares, social proof

---

## 📈 Best Practices

### Before Generating
✅ Fill in detailed features (more = better copy)
✅ Choose accurate market (affects tone)
✅ Set correct objective (Conversion for sales)

### After Generating
✅ Read all 3 variants
✅ Pick highest engagement score
✅ Tweak if needed (add brand name, etc.)
✅ Test multiple variants in Facebook

### For Best Results
✅ Emphasize unique benefits (not generic)
✅ Include specific numbers ("3 modes", "24-hour battery")
✅ Add product category context (helps AI)

---

## 🔗 API Endpoints

### `POST /scrape`
```bash
curl -X POST http://localhost:5000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://vigoshop.si/izdelek/product/"}'
```

### `POST /generate`
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Test Product",
    "price": "19.99€",
    "features": "Feature 1 | Feature 2",
    "market": "SI",
    "objective": "Conversion"
  }'
```

### `GET /examples`
```bash
curl http://localhost:5000/examples
```

### `GET /health`
```bash
curl http://localhost:5000/health
```

---

## 📚 Documentation Files

- **README.md**: Full setup and usage instructions
- **SUBMISSION.md**: Project overview for HS Plus team
- **ARCHITECTURE.md**: Technical architecture details
- **examples.txt**: 3 complete example outputs
- **QUICKSTART.md**: This file!

---

## ⚡ Pro Tips

1. **Batch Processing**: Open multiple tabs, queue 10+ products
2. **Template Fallback**: Works even if Claude API is down
3. **Copy Editing**: Feel free to tweak generated copy
4. **Example Products**: Use as templates for similar products
5. **Market Testing**: Generate same product for different markets
6. **Objective Testing**: Try all 3 objectives, compare results

---

## 🎯 Next Steps After Setup

1. ✅ Verify test_setup.py passes all checks
2. ✅ Load example products and generate copy
3. ✅ Test with a real vigoshop.si product
4. ✅ Compare variants, pick best one
5. ✅ Export and use in Facebook Ads Manager
6. ✅ Track performance and iterate

---

## 🆘 Getting Help

### Check Logs
```bash
# Backend logs (in Terminal 1)
# Look for errors after API calls

# Frontend console (in browser)
# Press F12 → Console tab
```

### Common Issues
| Issue | Solution |
|-------|----------|
| CORS error | Restart both backend + frontend |
| API timeout | Check internet, retry |
| Invalid URL | Must be vigoshop.si product page |
| Empty variants | Check .env has API key |

### Still Stuck?
1. Run `python test_setup.py`
2. Check `backend/.env` exists with API key
3. Verify ports 3000 and 5000 are free
4. Try example products first

---

## 🚀 Ready to Scale?

**For production deployment:**
1. See README.md → "Production Deployment" section
2. Use Docker: `docker-compose up -d`
3. Deploy to cloud (Vercel + AWS Lambda)
4. Add authentication and rate limiting

**For team use:**
1. Share .env template (without API key)
2. Document brand-specific tweaks
3. Create custom examples for your products
4. Track which variants perform best

---

## ✨ Happy Generating!

**Average time per ad copy:** 30 seconds
**Manual copywriting time saved:** 30 minutes → 30 seconds (60x faster)

Start creating high-converting Facebook ads in seconds! 🎉
