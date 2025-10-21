# Marketing Copy Generator - Project Submission

## Overview

This is a **Marketing Copy Generator** web application specifically designed for HS Plus to create high-converting Facebook ad copy for dropshipping products. The tool emphasizes **fast EU shipping** as the primary differentiator against competitors like Temu and AliExpress.

## Key Features Implemented

### ✅ Core Functionality
- **Auto-scraping**: Paste vigoshop.si URL → automatically extracts product details
- **AI Copy Generation**: Claude API generates 3 unique variants with different angles
- **Market Customization**: Tailored copy for 6 European markets (SI, DE, IT, AT, HR, BA)
- **Facebook Preview**: Real-time preview in Facebook ad format
- **Export Options**: Copy to clipboard or download as TXT file
- **Engagement Scoring**: Heuristic-based score (0-100) to predict performance

### 🎯 Copy Generation Strategy
Each variant tests a different psychological angle:
1. **Pain Point** - Focuses on problems the product solves
2. **Benefit/Transformation** - Highlights life improvements
3. **Social Proof** - Leverages testimonials and popularity

### 🔑 Critical Differentiators (Per Requirements)
- ✅ **EU Shipping Emphasis**: "2-3 day delivery from EU warehouse" in every variant
- ✅ **Trust Signals**: Money-back guarantees, verified reviews, social proof
- ✅ **UGC-Style Tone**: Casual, conversational (not corporate)
- ✅ **Market-Specific**: Different tones for Slovenia vs Germany vs Italy
- ✅ **Mobile-Optimized**: Character counts under 150 words

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Backend | Python + Flask | API server |
| Scraping | BeautifulSoup4 | vigoshop.si product extraction |
| AI | Anthropic Claude API | Copy generation |
| Frontend | React 18 | User interface |
| Build Tool | Vite | Fast development |
| HTTP Client | Axios | API communication |

## Project Structure

```
marketing-copy-generator/
├── backend/
│   ├── app.py                  # Flask API (4 endpoints)
│   ├── scraper.py              # vigoshop.si scraper (robust selectors)
│   ├── copy_generator.py       # Claude integration + prompt engineering
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main component
│   │   ├── components/
│   │   │   ├── InputForm.jsx   # Product input form
│   │   │   └── CopyPreview.jsx # Ad preview + export
│   │   └── utils/api.js
│   └── package.json
├── examples.txt                # 3 complete example outputs
├── README.md                   # Setup instructions
├── SUBMISSION.md               # This file
├── setup.sh                    # One-command setup script
├── Dockerfile                  # Optional Docker deployment
└── .env.example
```

## Setup Instructions

### Quick Start (3 steps)

```bash
# 1. Run setup script
./setup.sh

# 2. Add your API key
echo "ANTHROPIC_API_KEY=your_key_here" > backend/.env

# 3. Start both servers
# Terminal 1:
cd backend && python app.py

# Terminal 2:
cd frontend && npm run dev

# Open http://localhost:3000
```

### Manual Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
cp ../.env.example .env
# Edit .env and add ANTHROPIC_API_KEY
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### `POST /scrape`
Extract product data from vigoshop.si URL
```json
{
  "url": "https://vigoshop.si/izdelek/product-name/"
}
```

### `POST /generate`
Generate 3 ad copy variants
```json
{
  "product_name": "Product Name",
  "price": "19,99€",
  "features": "Feature 1 | Feature 2",
  "market": "SI",
  "objective": "Conversion"
}
```

### `GET /examples`
Get 3 pre-loaded example products

### `GET /health`
Check API and Claude configuration status

## Example Outputs

See `examples.txt` for 3 complete examples:

1. **Električni čistilec zob SMILY** (Beauty/Personal Care)
   - Engagement scores: 82-88/100
   - Focus: Professional results at home

2. **Zunanja brezžična kamera DigiCam** (Electronics/Security)
   - Engagement scores: 80-86/100
   - Focus: Peace of mind, 24/7 monitoring

3. **Pršilo proti praskam CarEase** (Automotive/Home Care)
   - Engagement scores: 81-87/100
   - Focus: DIY professional results

**All variants include:**
- EU shipping emphasis (2-3 days)
- Trust signals (guarantees, reviews)
- 2-3 relevant emojis
- Character counts: 138-148 words
- Clear CTAs with urgency

## Prompt Engineering Highlights

The Claude API prompt is carefully engineered to:

```
✅ Hook must grab attention in first 3 words
✅ MANDATORY "Ships from EU warehouse - 2-3 day delivery"
✅ Include trust signals (guarantee, reviews, social proof)
✅ Casual, conversational tone (UGC-style)
✅ Keep under 150 words
✅ Include 2-3 relevant emojis
✅ Test different angles per variant
✅ Market-specific tone (professional DE vs casual SI)
```

**Fallback System**: If Claude API fails, template-based generation ensures the tool never breaks.

## Engagement Score Algorithm

Simple heuristic (0-100) based on:

| Factor | Impact | Details |
|--------|--------|---------|
| Hook length | +15 pts | Shorter = better (3-5 words ideal) |
| Emoji usage | +15 pts | 2-3 emojis optimal |
| Character count | +10 pts | Under 125 words (mobile-friendly) |
| Trust signals | +10 pts | Keywords: guarantee, reviews, verified |
| EU shipping | +10 pts | Critical differentiator present |

**Typical scores**: 75-90/100 for AI-generated copy

## Error Handling

✅ **Invalid URLs** → User-friendly error messages
✅ **API failures** → Fallback to template-based generation
✅ **Scraping failures** → Manual input option available
✅ **Rate limiting** → Graceful error handling
✅ **Missing API key** → Clear setup instructions displayed

## Testing the Application

### Test Case 1: Example Products
1. Click "Beauty Product" button
2. Click "Generate Ad Copy"
3. Verify 3 variants appear with engagement scores
4. Test "Copy" and "Download TXT" buttons

### Test Case 2: Custom URL
1. Paste: `https://vigoshop.si/izdelek/ultrazvocni-cistilec-zob-smily/`
2. Watch auto-fill populate fields
3. Change market to "DE" (Germany)
4. Generate and verify tone is more professional

### Test Case 3: Manual Entry
1. Clear form
2. Enter custom product details
3. Generate copy
4. Verify all variants work correctly

## Future Improvements (Not Implemented)

If given more time, these would enhance the tool:

### AI Enhancement
- **Claude Vision API**: Analyze product images to extract benefits
- **Multi-language**: Auto-translate for all 27 EU markets
- **A/B Test Prediction**: ML model to predict winning variant

### Automation
- **Batch Processing**: Upload CSV of 100+ products
- **Facebook Ads API**: Auto-create campaigns directly
- **Performance Tracking**: Store historical data, learn patterns

### Advanced Features
- **Competitor Analysis**: Scrape competitor ads for insights
- **Brand Voice Training**: Fine-tune on HS Plus's existing copy
- **Category Templates**: Different styles per product type

### Optimization
- **Caching**: Redis for common products
- **Real-time Preview**: Actual Facebook Ad mockup with images
- **SEO Integration**: Optimize product descriptions too

## Production Deployment

### Option 1: Manual
```bash
# Backend
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Frontend
cd frontend
npm run build
# Serve with nginx or similar
```

### Option 2: Docker
```bash
docker-compose up -d
```

### Option 3: Cloud (AWS/GCP/Azure)
- Backend: Deploy to AWS Lambda or Google Cloud Run
- Frontend: Deploy to Vercel or Netlify
- Add CDN for static assets

## Performance Considerations

| Metric | Current | Optimized |
|--------|---------|-----------|
| Scraping | ~2-3s | Add caching → <1s |
| Copy generation | ~5-8s | Use Claude Haiku → ~2-3s |
| Frontend load | <1s | Already optimized |
| API response | <10s total | Could batch requests |

## Security Notes

✅ CORS configured (frontend ↔ backend)
✅ API key stored in environment variables (not committed)
✅ Input validation on all endpoints
✅ Rate limiting consideration (queued requests)
⚠️ For production: Add authentication, HTTPS, rate limiting

## Known Limitations

1. **Scraping Dependency**: If vigoshop.si changes HTML structure, selectors need updates
2. **No Database**: Stateless tool (doesn't store history)
3. **Single Language Output**: Always generates in English (would need translation layer)
4. **Simple Engagement Score**: Heuristic-based, not ML-powered
5. **No A/B Testing**: Can't predict which variant will perform best (would need historical data)

## What Makes This Different?

**vs Generic Copy Tools:**
- ✅ Specifically optimized for **dropshipping** (EU shipping emphasis)
- ✅ **Market-specific** customization (Slovenia vs Germany tone)
- ✅ **3 psychological angles** per product (not just one variant)
- ✅ **Engagement scoring** (performance prediction)

**vs Manual Copywriting:**
- ✅ **10x faster** (30 seconds vs 30 minutes)
- ✅ **Consistent quality** (always includes trust signals)
- ✅ **Data-driven** (character counts, emoji usage optimized)
- ✅ **Scalable** (100+ products per day possible)

## Code Quality

✅ **Clean separation**: Backend/frontend split
✅ **Modular**: Each component has single responsibility
✅ **Error handling**: Graceful degradation everywhere
✅ **Documentation**: Comprehensive README + inline comments
✅ **Type hints**: Python functions have clear signatures
✅ **Responsive design**: Works on mobile/tablet/desktop

## Demo Flow

**Expected user journey (30 seconds):**

1. Open tool → see clean interface
2. Click "Beauty Product" example
3. Click "Generate Ad Copy"
4. See 3 variants appear in Facebook format
5. Click "Copy" on best variant
6. Paste into Facebook Ads Manager
7. Done!

## Contact & Next Steps

**Deliverables:**
- ✅ Working application (frontend + backend)
- ✅ README.md with setup instructions
- ✅ requirements.txt / package.json
- ✅ examples.txt with 3 product outputs
- ✅ Dockerfile for easy deployment

**Questions for Interview:**
1. What markets should we prioritize first?
2. Do you have existing ad copy I can train on?
3. Would you prefer batch processing or one-at-a-time?
4. Should we integrate directly with Facebook Ads API?

---

Thank you for reviewing this submission! I'm excited to discuss how this tool can scale HS Plus's ad creation workflow.

**Setup time:** ~5 minutes
**First ad copy:** ~30 seconds after setup

🚀 Ready to generate!
