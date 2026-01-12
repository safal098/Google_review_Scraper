# Google Review Scraper - Pokhara

A comprehensive web scraper for extracting Google reviews from places, hotels, lakes, and viewpoints in Pokhara, Nepal. This project uses both Selenium-based web scraping and Google Places API methods to collect and analyze reviews.

## Features

- **Multi-Category Support**: Extract reviews for hotels, temples, restaurants, lakes, and viewpoints
- **Flexible Scraping Methods**: 
  - Selenium-based web scraping (no API key required)
  - Google Places API integration (with API key)l
- **Batch Processing**: Handle multiple locations and categories
- **Rate Limiting**: Built-in delays to prevent API throttling
- **CSV Export**: Store results in organized CSV files

## Project Structure

```
data/
├── Scraper/
│   ├── config.py                          # Configuration settings
│   ├── pokhara_google_reviews_scraper.py  # Main scraper implementation
│   ├── example_usage.py                   # Usage examples
│   └── __pycache__/
├── output_reviews/
│   ├── pokhara_reviews.csv                # All collected reviews
│   ├── pokhara_reviews_interim.csv        # Intermediate results
│   ├── pokhara_places.csv                 # Places metadata
│   └── pokhara_reviews_code_switched.csv  # Code-switched reviews
                     # Individual hotel review files                    # Trekking TikTok mentions
```

## Installation

### Prerequisites
- Python 3.8+
- Chrome browser (for Selenium scraping)
- Google Places API Key (for API-based scraping) - [Get your key](https://console.cloud.google.com/)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/safal098/Google_review_Scraper.git
cd Google_review_Scraper
```

2. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the scraper:
   - Open `data/Scraper/config.py`
   - Add your Google Places API key (if using API method)
   - Adjust search radius, delays, and other settings as needed

## Usage

### Basic Usage - Selenium Scraping (No API Key)

```python
from data.Scraper.pokhara_google_reviews_scraper import GoogleMapsSeleniumScraper

# Initialize scraper
scraper = GoogleMapsSeleniumScraper(output_dir='pokhara_reviews')

# Extract reviews for a specific place
scraper.scrape_place_reviews('Hotel Name', output_file='hotel_reviews.csv')

# Close the browser
scraper.close_driver()
```

### Using the API Method

```python
from data.Scraper.pokhara_google_reviews_scraper import PokharaReviewExtractor

# Initialize extractor
extractor = PokharaReviewExtractor()

# Extract all reviews
reviews_df = extractor.extract_all_reviews()

# Save to CSV
reviews_df.to_csv('all_reviews.csv', index=False)
```

## Configuration

Edit `data/Scraper/config.py` to customize:

- **API Key**: Your Google Places API key
- **Search Location**: Pokhara coordinates (latitude, longitude)
- **Search Radius**: Coverage area in meters (default: 25km)
- **Rate Limiting**: Delays between requests to prevent throttling
- **Categories**: Place types to search (hotels, restaurants, etc.)

## Data Output

The scraper generates CSV files with the following columns:

- `place_id`: Unique identifier for the place
- `place_name`: Name of the place
- `review_text`: Full review text
- `rating`: Review rating (1-5 stars)
- `reviewer_name`: Name of the reviewer
- `review_date`: Date the review was posted
- `review_count`: Number of reviews for the place
- `place_address`: Address of the place
- `place_type`: Category of the place

## Data Cleaning

Use the provided cleaning scripts in `cleaned data/` folder:

```python
import pandas as pd

# Load raw reviews
df = pd.read_csv('data/output_reviews/pokhara_reviews.csv')

# Remove duplicates and clean text
df = df.drop_duplicates()
df['review_text'] = df['review_text'].str.strip()

# Save cleaned data
df.to_csv('cleaned_reviews.csv', index=False)
```

## Code-Switching Analysis

The project includes support for analyzing code-switched content (Nepali-English mixing):

```python
# Nepali stopwords available in: data/cleaned data/NepaliStopWords.txt
# Nepali wordlist available in: data/cleaned data/nep.wordlist

# Remove stopwords from reviews
stopwords = set()
with open('data/cleaned data/NepaliStopWords.txt', 'r', encoding='utf-8') as f:
    stopwords = set(line.strip() for line in f)
```

## Requirements

See [requirements.txt](requirements.txt) for all dependencies.

Key packages:
- `selenium`: Web scraping
- `beautifulsoup4`: HTML parsing
- `pandas`: Data manipulation
- `requests`: HTTP requests
- `webdriver-manager`: Chrome driver management
- `tqdm`: Progress bars

## API Limits & Rate Limiting

- Google Places API has usage limits based on your plan
- Built-in rate limiting prevents overuse (configurable in config.py)
- Recommended delays:
  - Between requests: 0.5 seconds
  - Between batches: 2 seconds
  - For pagination: 2 seconds

## Error Handling

The scraper includes error handling for:
- Network timeouts
- Missing or invalid data
- API rate limits
- Invalid coordinates
- Browser crashes

## Performance Tips

1. **Reduce search radius** if only interested in central Pokhara
2. **Limit max places** in config.py to reduce extraction time
3. **Increase delays** if encountering API rate limits
4. **Use filtering** to focus on specific place types

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Citation

If you use this scraper in your research, please cite:

```bibtex
@software{pokhara_scraper_2025,
  author = {Safal Aryal},
  title = {Google Review Scraper - Pokhara},
  year = {2025},
  url = {https://github.com/safal098/Google_review_Scraper}
}
```

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Acknowledgments

- Google Places API documentation
- Selenium WebDriver
- Data collection for tourism and NLP research
- Code-switching analysis research

## Contact

For questions or issues, please open an issue on GitHub or contact the maintainer.

## Troubleshooting

### Common Issues

**Q: "API Key not found" error**
- Ensure you've added your Google Places API key in `config.py`

**Q: Chrome driver not found**
- `webdriver-manager` should auto-download it. If issues persist, install ChromeDriver manually.

**Q: Rate limit errors**
- Increase the `DELAY_BETWEEN_REQUESTS` value in `config.py`

**Q: No reviews found**
- Check internet connection and Google Maps accessibility in your region
- Verify place names are correct
- Try increasing the search radius

## Updates & Changelog

**v1.0 (2025-12-29)**
- Initial release with Selenium-based scraping
- Google Places API integration
- Data cleaning and preprocessing
- Code-switching analysis support
