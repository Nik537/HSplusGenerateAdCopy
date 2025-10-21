# Marketing Copy Generator - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         USER BROWSER                         │
│                    http://localhost:3000                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    REACT FRONTEND (Vite)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  InputForm   │  │ CopyPreview  │  │  API Client  │      │
│  │ - Product URL│  │ - 3 Variants │  │  (Axios)     │      │
│  │ - Form fields│  │ - FB Preview │  │              │      │
│  │ - Examples   │  │ - Export     │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ REST API
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   FLASK BACKEND (Python)                     │
│                   http://localhost:5000                      │
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │ API ENDPOINTS                                       │     │
│  │  • GET  /health     - Health check                 │     │
│  │  • POST /scrape     - Scrape vigoshop.si           │     │
│  │  • POST /generate   - Generate ad copy             │     │
│  │  • GET  /examples   - Get example products         │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Scraper    │  │ Copy Generator│ │   Examples   │      │
│  │              │  │                │ │              │      │
│  │ - Parse HTML │  │ - Claude API  │ │ - Predefined │      │
│  │ - Extract    │  │ - Prompt      │ │ - 3 products │      │
│  │   data       │  │ - Fallback    │ │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
         │                      │
         │                      │
         ▼                      ▼
┌──────────────┐      ┌──────────────────────┐
│ vigoshop.si  │      │  Anthropic Claude    │
│              │      │  API (Sonnet 3.5)    │
│ - Product    │      │                      │
│   pages      │      │  - Copy generation   │
│ - WooComm.   │      │  - Prompt engineer.  │
└──────────────┘      └──────────────────────┘
```

## Data Flow

### 1. Scraping Flow
```
User pastes URL
    ↓
Frontend sends POST to /scrape
    ↓
Backend: VigoShopScraper.scrape_product()
    ↓
HTTP GET to vigoshop.si
    ↓
BeautifulSoup parses HTML
    ↓
Extract: name, price, image, features, description
    ↓
Return JSON to frontend
    ↓
Auto-fill form fields
```

### 2. Copy Generation Flow
```
User clicks "Generate Ad Copy"
    ↓
Frontend validates form data
    ↓
POST to /generate with:
  - product_name
  - price
  - features
  - market (SI/DE/IT/AT/HR/BA)
  - objective (Awareness/Conversion/Engagement)
    ↓
Backend: CopyGenerator.generate_ad_copy()
    ↓
Build prompt with market-specific context
    ↓
Call Claude API (claude-3-5-sonnet-20241022)
    ↓
Parse JSON response
    ↓
Calculate engagement scores for each variant
    ↓
Return 3 variants to frontend
    ↓
Display in Facebook ad format
```

### 3. Example Products Flow
```
Component mounts
    ↓
Frontend calls GET /examples
    ↓
Backend returns 3 pre-defined products
    ↓
User clicks "Load Example" button
    ↓
Auto-fill form with example data
    ↓
User can immediately generate
```

## Component Breakdown

### Frontend (React)

**App.jsx** (Main Controller)
- State management (formData, variants, loading, error)
- API communication
- Auto-scrape on URL change
- Error handling

**InputForm.jsx**
- Product URL input
- Manual fields (name, price, features)
- Market dropdown (6 options)
- Objective dropdown (3 options)
- Example buttons (3 products)
- Form validation

**CopyPreview.jsx**
- Empty state (no variants yet)
- 3 variant cards
- Facebook ad mockup
- Engagement score display
- Copy to clipboard
- Download as TXT

**api.js** (API Client)
- Axios configuration
- 4 API methods
- Error handling

### Backend (Python)

**app.py** (Flask Server)
- CORS configuration
- 4 route handlers
- Request validation
- Error responses
- Service initialization

**scraper.py** (Web Scraper)
- VigoShopScraper class
- Multiple CSS selector fallbacks
- Robust error handling
- Product data extraction

**copy_generator.py** (AI Integration)
- CopyGenerator class
- Claude API client
- Prompt engineering
- JSON parsing
- Engagement score calculation
- Template fallback

## Prompt Engineering Architecture

### Input → Prompt Builder
```
Product Data + Market + Objective
    ↓
Market-Specific Context Injection
  SI: "casual Slovenian, local trust"
  DE: "professional, quality focus"
  IT: "warm, family-oriented"
  AT: "reliable, quality"
    ↓
Objective Optimization
  Awareness: Broader reach, curiosity
  Conversion: Direct CTA, urgency
  Engagement: Social proof, sharing
    ↓
Build Structured Prompt
  - Product context
  - Requirements (EU shipping, trust signals)
  - Format instructions (JSON)
  - 3 variant angles
    ↓
Send to Claude API
```

### Claude API → Response Parser
```
Claude generates JSON response
    ↓
Extract from code blocks (```json)
    ↓
Parse JSON
    ↓
Validate structure
  - variant_1, variant_2, variant_3
  - Each has: angle, hook, body, cta, character_count
    ↓
Calculate engagement scores
  - Hook length
  - Emoji count
  - Character count
  - Trust signals
  - EU shipping mention
    ↓
Return enriched variants
```

## Engagement Score Algorithm

```python
Base score: 50 points

+ Hook length (15 pts max)
  - 3 words or less: +15
  - 4-5 words: +10
  - 6+ words: +5

+ Emoji usage (15 pts max)
  - 2-3 emojis: +15
  - 1 or 4 emojis: +10
  - Other: +5

+ Character count (10 pts max)
  - Under 125: +10
  - 125-150: +5

+ Trust signals (10 pts)
  - Contains: guarantee, reviews, verified, etc.

+ EU shipping (10 pts)
  - Contains: eu warehouse, fast delivery, etc.

= Final Score (0-100)
```

## Error Handling Strategy

### Frontend
```
API Call Error
    ↓
Catch in try/catch
    ↓
Extract error message from response
    ↓
Display error banner at top
    ↓
Allow user to dismiss or retry
```

### Backend
```
Request Error
    ↓
Try operation
    ↓
Catch specific exceptions
  - ValueError: Invalid input
  - RequestException: HTTP errors
  - JSONDecodeError: Parse errors
  - Exception: Generic fallback
    ↓
Return JSON error response
  {
    "success": false,
    "error": "Descriptive message"
  }
    ↓
Appropriate HTTP status code
  - 400: Bad request
  - 500: Server error
```

### Claude API Fallback
```
Claude API fails (timeout, rate limit, etc.)
    ↓
Catch exception
    ↓
Log error
    ↓
Call _generate_template_copy()
    ↓
Return 3 pre-built variants
  - Uses product data
  - Generic but functional
  - Ensures tool never breaks
```

## Deployment Options

### Option 1: Local Development
```
Backend:  python app.py (port 5000)
Frontend: npm run dev (port 3000)
Access:   http://localhost:3000
```

### Option 2: Docker Compose
```
Backend:  Docker container (port 5000)
Frontend: Docker container (port 3000)
Network:  Internal docker network
Access:   http://localhost:3000
```

### Option 3: Production (Cloud)
```
Backend:  AWS Lambda / Cloud Run
          API Gateway
          Environment variables (API key)

Frontend: Vercel / Netlify
          CDN for static assets
          Environment: production build

Database: (Optional) Redis for caching
          PostgreSQL for history
```

## Security Considerations

### Current Implementation
✅ CORS configured (specific origin)
✅ Environment variables for secrets
✅ Input validation on all endpoints
✅ No SQL injection risk (no database)
✅ Rate limiting consideration (queued requests)

### Production Additions
- [ ] Add authentication (API keys for users)
- [ ] HTTPS only
- [ ] Rate limiting per IP/user
- [ ] Request size limits
- [ ] API key rotation
- [ ] Audit logging
- [ ] DDoS protection

## Performance Optimizations

### Current
- Vite for fast frontend builds
- Single scraping request per URL
- Efficient BeautifulSoup parsing
- JSON responses (lightweight)

### Future
- Redis caching for common products
- CDN for static assets
- Gzip compression
- Database indexing (if added)
- Batch processing endpoint
- WebSocket for real-time updates

## Monitoring & Logging

### Backend Logging Points
1. Scraping start/success/failure
2. Claude API calls (duration, tokens)
3. Error responses
4. Health check status

### Frontend Logging Points
1. API call timings
2. User actions (button clicks)
3. Error displays
4. Example loads

### Metrics to Track (Production)
- Scraping success rate
- Claude API response time
- Average engagement scores
- Most common errors
- Popular example products
- Market distribution (SI vs DE vs IT)
