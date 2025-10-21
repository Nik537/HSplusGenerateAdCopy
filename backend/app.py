from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from scraper import VigoShopScraper
from copy_generator import CopyGenerator

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS to allow Firebase frontend and local development
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://hsplusfbadscopy.web.app",
            "https://hsplusfbadscopy.firebaseapp.com",
            "http://localhost:5173",
            "http://localhost:3000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Initialize services
scraper = VigoShopScraper()
copy_generator_error = None

# Debug: Check anthropic version
try:
    import anthropic
    anthropic_version = anthropic.__version__
    print(f"Anthropic library version: {anthropic_version}")
except Exception as e:
    anthropic_version = f"Error: {e}"

try:
    copy_generator = CopyGenerator()
except Exception as e:
    import traceback
    copy_generator_error = f"{str(e)} | anthropic_version={anthropic_version}"
    print(f"Warning: Failed to initialize CopyGenerator: {e}")
    print(f"Anthropic version: {anthropic_version}")
    print(traceback.format_exc())
    copy_generator = None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    anthropic_configured = copy_generator and copy_generator.anthropic_client is not None

    # Debug: Check if env vars are set
    anthropic_key_exists = bool(os.getenv('ANTHROPIC_API_KEY'))

    return jsonify({
        'status': 'healthy',
        'claude_api_configured': anthropic_configured,
        'any_api_configured': anthropic_configured,
        'debug': {
            'anthropic_env_var_exists': anthropic_key_exists,
            'copy_generator_exists': copy_generator is not None,
            'initialization_error': copy_generator_error
        }
    })

@app.route('/scrape', methods=['POST'])
def scrape_product():
    """
    Scrape product data from vigoshop.si URL

    Request body:
    {
        "url": "https://vigoshop.si/izdelek/product-name/"
    }

    Returns:
    {
        "success": true,
        "data": {
            "url": "...",
            "name": "...",
            "price": "...",
            "image_url": "...",
            "features": "...",
            "description": "...",
            "category": "..."
        }
    }
    """
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({
                'success': False,
                'error': 'URL is required'
            }), 400

        # Scrape product
        product_data = scraper.scrape_product(url)

        return jsonify({
            'success': True,
            'data': product_data
        })

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to scrape product: {str(e)}'
        }), 500

@app.route('/generate', methods=['POST'])
def generate_copy():
    """
    Generate Facebook ad copy variants

    Request body:
    {
        "product_name": "Product Name",
        "price": "19.99€",
        "features": "Feature 1 | Feature 2 | Feature 3",
        "market": "SI",
        "objective": "Conversion",
        "description": "Optional full description"
    }

    Returns:
    {
        "success": true,
        "data": {
            "variant_1": { ... },
            "variant_2": { ... },
            "variant_3": { ... }
        }
    }
    """
    try:
        if not copy_generator:
            return jsonify({
                'success': False,
                'error': 'Claude API not configured. Please set ANTHROPIC_API_KEY environment variable.'
            }), 500

        data = request.get_json()

        # Validate required fields
        required_fields = ['product_name', 'price', 'features', 'market', 'objective']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400

        # Generate copy
        variants = copy_generator.generate_ad_copy(
            product_name=data['product_name'],
            price=data['price'],
            features=data['features'],
            market=data['market'],
            objective=data['objective'],
            description=data.get('description', ''),
            model=data.get('model', 'claude-haiku'),  # Default to Claude Haiku 4.5
            max_chars=data.get('max_chars', 150)  # Default to 150 characters
        )

        return jsonify({
            'success': True,
            'data': variants
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to generate copy: {str(e)}'
        }), 500

@app.route('/examples', methods=['GET'])
def get_examples():
    """
    Get pre-defined example products

    Returns:
    {
        "examples": [
            {
                "name": "Example 1",
                "url": "...",
                "product_name": "...",
                ...
            }
        ]
    }
    """
    examples = [
        {
            "name": "Beauty/Personal Care",
            "url": "https://vigoshop.si/izdelek/ultrazvocni-cistilec-zob-smily/",
            "product_name": "Električni čistilec zob SMILY",
            "price": "19,99€",
            "features": "Removes plaque and stains | Ultrasonic technology | USB rechargeable | 3 cleaning modes",
            "market": "SI",
            "objective": "Conversion",
            "category": "Beauty & Health"
        },
        {
            "name": "Electronics/Home Security",
            "url": "https://vigoshop.si/izdelek/zunanja-brezzicna-kamera-digicam/",
            "product_name": "Zunanja brezžična kamera DigiCam",
            "price": "49,99€",
            "features": "Wireless outdoor camera | Night vision | Motion detection | Weatherproof | Mobile app",
            "market": "SI",
            "objective": "Awareness",
            "category": "Electronics"
        },
        {
            "name": "Automotive/Home Care",
            "url": "https://vigoshop.si/izdelek/prsilo-proti-praskam-na-avtomobilu-carease/",
            "product_name": "Pršilo proti praskam CarEase",
            "price": "24,99€",
            "features": "Removes scratches instantly | No rubbing needed | Works on all colors | Professional results | Easy to use",
            "market": "SI",
            "objective": "Engagement",
            "category": "Automotive"
        }
    ]

    return jsonify({
        'success': True,
        'examples': examples
    })

if __name__ == '__main__':
    # Check for API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("\n⚠️  WARNING: ANTHROPIC_API_KEY not set!")
        print("Copy .env.example to .env and add your API key\n")

    # Railway needs host=0.0.0.0 and PORT env variable
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
