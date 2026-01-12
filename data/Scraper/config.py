"""
Configuration File for Pokhara Google Reviews Scraper
====================================================

This file contains all configuration settings for the scraper.
Replace the placeholder values with your actual credentials and preferences.

Author: AI Assistant
Date: 2025-12-29
"""

# =============================================================================
# REQUIRED: GOOGLE PLACES API CONFIGURATION
# =============================================================================

# ⚠️ IMPORTANT: Replace with your actual Google Places API Key
# Get your API key from: https://console.cloud.google.com/
# Steps:
# 1. Create a new project
# 2. Enable billing (required)
# 3. Enable "Places API" from the library
# 4. Create credentials → API key
# 5. Copy and paste below

GOOGLE_API_KEY = "AIzaSyCACkhakg7_kfOVuJhFenhCP85UgVTPMhw"

# =============================================================================
# SEARCH CONFIGURATION
# =============================================================================

# Pokhara city coordinates (center point)
# These coordinates cover the entire Pokhara valley
POKHARA_COORDINATES = {
    'lat': 28.2096,  # Latitude of Pokhara city center
    'lng': 83.9856   # Longitude of Pokhara city center
}

# Search radius in meters
# 25km covers all of Pokhara valley including nearby areas
SEARCH_RADIUS = 25000

# Maximum number of places to extract per category
# Reduce this number for faster extraction or to stay within API limits
MAX_PLACES_PER_CATEGORY = 50

# Rate limiting delays (in seconds)
# Increase these if you encounter rate limit errors
DELAY_BETWEEN_REQUESTS = 0.5      # Delay between individual API calls
DELAY_BETWEEN_BATCHES = 2.0       # Delay after every 10 requests
DELAY_FOR_PAGINATION = 2.0        # Delay when fetching next page of results

# =============================================================================
# PLACE CATEGORIES TO SEARCH
# =============================================================================

# Google Places API types to search for
# Modify these categories based on your needs
PLACE_CATEGORIES = {
    'hotels': ['lodging', 'hotel', 'motel', 'guest_house'],
    'lakes': ['natural_feature', 'lake', 'body_of_water'],
    'viewpoints': ['point_of_interest', 'establishment', 'tourist_attraction'],
    'restaurants': ['restaurant', 'food', 'cafe', 'bakery', 'meal_takeaway'],
    'attractions': ['tourist_attraction', 'amusement_park', 'museum', 'art_gallery'],
    'temples': ['place_of_worship', 'hindu_temple', 'church', 'mosque'],
    'adventure': ['campground', 'park', 'hiking_area', 'sports_complex'],
    'shopping': ['shopping_mall', 'store', 'department_store'],
    'transport': ['transit_station', 'airport', 'bus_station', 'taxi_stand']
}

# =============================================================================
# SPECIFIC PLACES TO SEARCH
# =============================================================================

# Specific places to search by name
# These are searched in addition to category-based searches
SPECIFIC_PLACES = {
    'hotels': [
        'Fish Tail Lodge', 'Tiger Mountain Pokhara Lodge',
        'Temple Tree Resort', 'The Pavilions Himalayas', 'Shangri-La Village Pokhara',
        'Hotel Landmark Pokhara', 'Mount Kailash Resort', 'Hotel Pokhara Grande',
        'Fulgur Guesthouse', 'Saraan Hotels', 'Hotel Middle Path',
        'Hotel Lake Star', 'Noble Inn', 'Hotel Peninsula', 'Hotel Lake Paradise',
        'Hotel Fewa Prince', 'Hotel Orchid', 'Hotel Diplomat', 'Hotel Tulsi',
        'Hotel Meera', 'Hotel Snowland', 'Hotel Peaceful', 'Hotel Blue Heaven'
    ],
    
    'lakes': [
        'Phewa Lake', 'Begnas Lake', 'Rupa Lake', 'Dipang Lake',
        'Khaste Lake', 'Maidi Lake', 'Neureni Lake', 'Gude Lake',
        'Kamalpokhari', 'Thuli Lake', 'Budhi Lake', 'Majh Lake'
    ],
    
    'viewpoints': [
        'World Peace Pagoda', 'Sarangkot Viewpoint', 'Kahun Danda',
        'Naudanda Viewpoint', 'Pumdikot Hill', 'Anadu Hill',
        'Bat Cave Pokhara', 'Mahendra Cave', 'Gupteshwor Mahadev Cave',
        'Seti River Gorge', 'Phewa Lake Viewpoint', 'Hemja Viewpoint'
    ],
    
    'temples': [
        'Tal Barahi Temple', 'Bindhyabasini Temple', 'Bhadrakali Temple',
        'Sitaladevi Temple', 'Gorakhnath Temple', 'Kedareshwar Temple',
        'Jangchub Choeling Monastery', 'Matepani Gumba', 'Shanti Stupa'
    ],
    
    'attractions': [
        'Devis Fall', 'Gurkha Memorial Museum', 'Pokhara Regional Museum',
        'International Mountain Museum', 'Phewa Lake Boating',
        'Paragliding Pokhara', 'ZipFlyer Nepal', 'Annapurna Butterfly Museum',
        'Pokhara Zipline', 'Ultra Light Flight Pokhara', 'Hot Air Balloon Pokhara',
        'Begnas Lake Boating', 'Rupa Lake Boating', 'Pokhara Skydiving'
    ],
    
    'restaurants': [
        'Moondance Restaurant', 'Caffe Concerto', 'OR2K Pokhara',
        'Himalayan Java Coffee', 'Punjabi Restaurant', 'Nepali Kitchen',
        'Lakeside Restaurant', 'Boomerang Restaurant', 'Almonds Café',
        'Perky Beans', 'Roadhouse Café', 'La Bella Napoli'
    ],
    
    'shopping': [
        'Pokhara Mall', 'Lakeside Bazaar', 'Tibetan Market Pokhara',
        'Ratna Market', 'Maya Handicrafts', 'Fairfax Pokhara'
    ],
    
    'transport': [
        'Pokhara Airport', 'Pokhara Tourist Bus Park', 'Prithvi Highway Bus Stop',
        'Lakeside Taxi Stand', 'Pokhara Regional Transport Office'
    ]
}

# =============================================================================
# OUTPUT CONFIGURATION
# =============================================================================

# Output directory for saving results
OUTPUT_DIRECTORY = 'D:\\Research work\\data\\output_reviews'

# File naming pattern
# Files will be saved as: pokhara_reviews_YYYYMMDD_HHMMSS.csv
FILE_TIMESTAMP_FORMAT = '%Y%m%d_%H%M%S'

# Export options
SAVE_REVIEWS_CSV = True          # Save reviews to CSV
SAVE_PLACES_CSV = True           # Save places to CSV
SAVE_SUMMARY_JSON = True         # Save extraction summary to JSON
CREATE_VISUALIZATIONS = True     # Create charts and graphs
EXPORT_TO_GOOGLE_DRIVE = False   # Auto-export to Google Drive

# =============================================================================
# WEB SCRAPING CONFIGURATION (Alternative Method)
# =============================================================================

# Chrome driver settings
# Chrome driver settings
CHROME_OPTIONS = [
    # '--headless',           # Run Chrome in headless mode (Disable for visible scraping)
    '--no-sandbox',         # Disable sandbox for Colab compatibility
    '--disable-dev-shm-usage',  # Disable shared memory usage
    '--disable-gpu',        # Disable GPU acceleration
    '--start-maximized',    # Start maximized
    # '--lang=en-US'          # Force English language (Commented to match system locale/tem.py)
]

# Web scraping delays
WEB_SCRAPE_DELAY_INITIAL = 3     # Initial page load delay
WEB_SCRAPE_DELAY_SCROLL = 2      # Delay when scrolling for reviews
WEB_SCRAPE_MAX_REVIEWS = 50     # Maximum reviews to scrape per place

# =============================================================================
# SENTIMENT ANALYSIS CONFIGURATION
# =============================================================================

# Sentiment classification thresholds
SENTIMENT_POSITIVE_THRESHOLD = 0.1    # Polarity > 0.1 = Positive
SENTIMENT_NEGATIVE_THRESHOLD = -0.1   # Polarity < -0.1 = Negative
# Between -0.1 and 0.1 = Neutral

# =============================================================================
# VISUALIZATION CONFIGURATION
# =============================================================================

# Chart colors
CHART_COLOR_PALETTE = 'husl'  # Color palette for charts
PIE_CHART_COLORS = 'Set3'     # Colors for pie charts
BAR_CHART_COLOR = 'skyblue'   # Default bar chart color
HISTOGRAM_COLOR = 'lightgreen'  # Histogram color

# Chart dimensions
FIGURE_WIDTH = 16
FIGURE_HEIGHT = 12
DPI = 300  # Resolution for saved images

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

# Enable/disable detailed logging
VERBOSE_LOGGING = True
LOG_TO_FILE = False
LOG_FILE_PATH = '/content/pokhara_reviews/extraction.log'

# =============================================================================
# VALIDATION
# =============================================================================

def validate_config():
    """Validate configuration settings"""
    errors = []
    
    # Check API key
    if GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY_HERE" or not GOOGLE_API_KEY:
        errors.append("❌ GOOGLE_API_KEY must be replaced with your actual API key")
    
    # Check coordinates
    if not isinstance(POKHARA_COORDINATES, dict):
        errors.append("❌ POKHARA_COORDINATES must be a dictionary with 'lat' and 'lng' keys")
    elif 'lat' not in POKHARA_COORDINATES or 'lng' not in POKHARA_COORDINATES:
        errors.append("❌ POKHARA_COORDINATES must contain 'lat' and 'lng' keys")
    
    # Check search radius
    if not isinstance(SEARCH_RADIUS, (int, float)) or SEARCH_RADIUS <= 0:
        errors.append("❌ SEARCH_RADIUS must be a positive number")
    
    # Check max places
    if not isinstance(MAX_PLACES_PER_CATEGORY, int) or MAX_PLACES_PER_CATEGORY <= 0:
        errors.append("❌ MAX_PLACES_PER_CATEGORY must be a positive integer")
    
    # Print validation results
    if errors:
        print("❌ Configuration validation failed:")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print("✅ Configuration validation passed!")
        return True

# Run validation when config is imported
if __name__ == "__main__":
    validate_config()

# =============================================================================
# END OF CONFIGURATION
# =============================================================================
