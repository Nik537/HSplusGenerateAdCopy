# Marketing Copy Generator for Facebook Ads

A web application that generates high-converting Facebook ad copy for dropshipping products, with a focus on European markets. Built specifically for HS Plus to compete against Temu/AliExpress by emphasizing fast EU shipping.

## Features

- **Auto-scraping**: Paste a vigoshop.si URL and automatically extract product details
- **AI-powered copy generation**: Uses Claude API to generate 3 unique ad variants
- **Multiple angles**: Each variant tests a different approach (pain point, benefit, social proof)
- **Market customization**: Tailored copy for different European markets (SI, DE, IT, AT, HR, BA)
- **Facebook preview**: See exactly how your ad will look on Facebook
- **Export options**: Copy to clipboard or download as TXT
- **Engagement scoring**: Simple heuristic to estimate ad performance

## Tech Stack

**Backend:**
- Python 3.8+
- Flask (API server)
- BeautifulSoup4 (web scraping)
- Anthropic Claude API (copy generation)

**Frontend:**
- React 18
- Vite (build tool)
- Axios (HTTP client)

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Installation

1. **Clone the repository**
```bash
cd marketing-copy-generator
```

2. **Set up backend**
```bash
cd backend
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

4. **Set up frontend**
```bash
cd ../frontend
npm install
```

### Running the Application

1. **Start the backend server** (in `backend/` directory)
```bash
python app.py
```
Server will run on `http://localhost:5000`

2. **Start the frontend** (in `frontend/` directory, new terminal)
```bash
npm run dev
```
Frontend will run on `http://localhost:3000`

3. **Open your browser**
Navigate to `http://localhost:3000`

## Usage

### Quick Start with Examples

1. Click one of the "Load Example" buttons (Beauty Product, Electronics, Automotive)
2. Click "Generate Ad Copy"
3. Review the 3 generated variants
4. Copy to clipboard or download as TXT

### Custom Product

1. Paste a vigoshop.si product URL (product details will auto-fill)
   - OR manually enter product name, price, and features
2. Select target market (Slovenia, Germany, Italy, etc.)
3. Choose ad objective (Awareness, Conversion, Engagement)
4. Click "Generate Ad Copy"
5. Export your favorite variant

## Project Structure

```
marketing-copy-generator/
├── backend/
│   ├── app.py                  # Flask API server
│   ├── scraper.py              # vigoshop.si scraper
│   ├── copy_generator.py       # Claude API integration
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main application component
│   │   ├── components/
│   │   │   ├── InputForm.jsx   # Product input form
│   │   │   └── CopyPreview.jsx # Ad copy preview & export
│   │   └── utils/
│   │       └── api.js          # API client
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── .env.example                # Environment variables template
├── .gitignore
├── README.md
└── examples.txt                # Example generated outputs
```

## API Endpoints

### `POST /scrape`
Extract product data from vigoshop.si URL

**Request:**
```json
{
  "url": "https://vigoshop.si/izdelek/product-name/"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "name": "Product Name",
    "price": "19,99€",
    "image_url": "https://...",
    "features": "Feature 1 | Feature 2 | Feature 3",
    "description": "...",
    "category": "Electronics"
  }
}
```

### `POST /generate`
Generate Facebook ad copy variants

**Request:**
```json
{
  "product_name": "Product Name",
  "price": "19,99€",
  "features": "Feature 1 | Feature 2",
  "market": "SI",
  "objective": "Conversion",
  "description": "Optional description"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "variant_1": {
      "angle": "pain_point",
      "hook": "Tired of waiting?",
      "body": "Get your Product delivered in just 2-3 days...",
      "cta": "Shop Now!",
      "character_count": 145,
      "engagement_score": 78
    },
    "variant_2": { ... },
    "variant_3": { ... }
  }
}
```

### `GET /examples`
Get pre-defined example products

### `GET /health`
Health check endpoint

## Copy Generation Strategy

Each generated variant emphasizes:

1. **Fast EU Shipping** - Main differentiator vs Temu/AliExpress
2. **Trust Signals** - Money-back guarantee, verified reviews
3. **Market-specific tone** - Casual for SI/HR, professional for DE/AT
4. **UGC-style language** - Authentic, not corporate
5. **Clear CTA** - Strong call-to-action

### Variant Angles

- **Variant 1 (Pain Point)**: Focuses on the problem the product solves
- **Variant 2 (Benefit)**: Highlights transformation/improvement
- **Variant 3 (Social Proof)**: Uses testimonials/popularity

## Engagement Score Calculation

Simple heuristic based on:
- Hook length (shorter is better: 3-5 words)
- Emoji usage (ideal: 2-3 emojis)
- Character count (under 125 words for mobile)
- Trust signals present (guarantee, reviews, etc.)
- EU shipping mention (mandatory)

Score range: 0-100 (higher is better)

## Example Products

The application includes 3 pre-loaded examples:

1. **Električni čistilec zob SMILY** - Beauty/Personal Care
2. **Zunanja brezžična kamera DigiCam** - Electronics/Security
3. **Pršilo proti praskam CarEase** - Automotive/Home Care

## Troubleshooting

### "API not configured" error
- Make sure you've created `.env` file in `backend/` directory
- Add your `ANTHROPIC_API_KEY=sk-ant-...`
- Restart the backend server

### Scraping fails
- Verify the URL is from vigoshop.si
- Website structure may have changed (update selectors in `scraper.py`)
- Try manually entering product details

### CORS errors
- Ensure backend is running on port 5000
- Frontend proxy is configured in `vite.config.js`

## Future Improvements

### AI Enhancement
- Image analysis with Claude Vision API
- Multi-language support (auto-translate for different markets)
- A/B test prediction model

### Automation
- Batch processing (CSV upload)
- Facebook Ads API integration (auto-create campaigns)
- Historical performance tracking

### Advanced Features
- Competitor analysis (scrape competitor ads)
- Custom brand voice training
- Dynamic templating per product category

## License

This project is proprietary software developed for HS Plus.

## Contact

For questions or support, contact the development team.
