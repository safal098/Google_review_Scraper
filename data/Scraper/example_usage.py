"""
Example Usage Script for Pokhara Google Reviews Scraper
======================================================

This script demonstrates various ways to use the scraper for different purposes.

Author: AI Assistant
Date: 2025-12-29
"""

# =============================================================================
# EXAMPLE 1: BASIC USAGE - EXTRACT ALL REVIEWS
# =============================================================================

def example_basic_usage():
    """
    Example 1: Basic usage - extract all reviews for all categories
    """
    print("="*80)
    print("EXAMPLE 1: BASIC USAGE - EXTRACT ALL REVIEWS")
    print("="*80)
    
    # Import required modules
    import sys
    sys.path.append('/path/to/scraper')  # Add path if needed
    
    from pokhara_google_reviews_scraper import PokharaReviewExtractor
    from config import GOOGLE_API_KEY
    
    # Check if API key is configured
    if GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY_HERE":
        print("❌ Please replace 'YOUR_GOOGLE_API_KEY_HERE' with your actual API key")
        return
    
    # Initialize extractor
    extractor = PokharaReviewExtractor(GOOGLE_API_KEY)
    
    # Extract reviews for all categories
    # This will search for all place types and specific places
    print("Extracting reviews for all categories...")
    extractor.extract_all_reviews(max_places_per_category=50)
    
    # Save data
    output_dir = extractor.save_data()
    
    print(f"✅ Extraction complete! Data saved to: {output_dir}")
    print(f"Total places: {len(extractor.places_data)}")
    print(f"Total reviews: {len(extractor.all_reviews)}")


# =============================================================================
# EXAMPLE 2: EXTRACT SPECIFIC CATEGORIES ONLY
# =============================================================================

def example_specific_categories():
    """
    Example 2: Extract only hotels and restaurants
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: EXTRACT SPECIFIC CATEGORIES ONLY")
    print("="*80)
    
    from pokhara_google_reviews_scraper import PokharaReviewExtractor, GoogleReviewsConfig
    from config import GOOGLE_API_KEY
    
    if GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY_HERE":
        print("❌ Please configure your API key first")
        return
    
    # Create custom configuration
    config = GoogleReviewsConfig()
    
    # Override categories to search only hotels and restaurants
    config.PLACE_CATEGORIES = {
        'hotels': ['lodging', 'hotel'],
        'restaurants': ['restaurant', 'food', 'cafe']
    }
    
    # Initialize extractor with custom config
    extractor = PokharaReviewExtractor(GOOGLE_API_KEY)
    extractor.config = config
    
    # Extract reviews
    print("Extracting reviews for hotels and restaurants only...")
    extractor.extract_all_reviews(max_places_per_category=30)
    
    # Save data
    output_dir = extractor.save_data()
    print(f"✅ Data saved to: {output_dir}")


# =============================================================================
# EXAMPLE 3: EXTRACT REVIEWS FOR SPECIFIC PLACES
# =============================================================================

def example_specific_places():
    """
    Example 3: Extract reviews for specific places only
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: EXTRACT REVIEWS FOR SPECIFIC PLACES")
    print("="*80)
    
    from pokhara_google_reviews_scraper import PokharaReviewExtractor, GooglePlacesClient
    from config import GOOGLE_API_KEY, POKHARA_COORDINATES, SEARCH_RADIUS
    
    if GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY_HERE":
        print("❌ Please configure your API key first")
        return
    
    # Initialize client
    client = GooglePlacesClient(GOOGLE_API_KEY)
    
    # Define specific places to search
    specific_places = [
        'Hotel Barahi Pokhara',
        'Phewa Lake Pokhara',
        'Sarangkot Viewpoint',
        'World Peace Pagoda Pokhara'
    ]
    
    all_reviews = []
    all_places = []
    
    print("Searching for specific places...")
    for place_name in specific_places:
        print(f"Searching for: {place_name}")
        
        # Search for place
        results = client.text_search(
            query=place_name,
            location=POKHARA_COORDINATES,
            radius=SEARCH_RADIUS
        )
        
        if results:
            # Get details for first result
            place = results[0]
            details = client.get_place_details(place['place_id'])
            
            if details:
                # Extract place info
                place_info = {
                    'place_id': place['place_id'],
                    'name': details.get('name', place_name),
                    'address': details.get('formatted_address', 'N/A'),
                    'rating': details.get('rating', 0),
                    'total_ratings': details.get('user_ratings_total', 0),
                    'latitude': details.get('geometry', {}).get('location', {}).get('lat', 0),
                    'longitude': details.get('geometry', {}).get('location', {}).get('lng', 0),
                    'search_category': 'specific_search',
                    'extraction_date': __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                all_places.append(place_info)
                
                # Extract reviews
                reviews = details.get('reviews', [])
                for review in reviews:
                    review_data = {
                        'place_id': place['place_id'],
                        'place_name': place_info['name'],
                        'reviewer_name': review.get('author_name', 'Anonymous'),
                        'rating': review.get('rating', 0),
                        'review_text': review.get('text', ''),
                        'review_time': review.get('relative_time_description', ''),
                        'extraction_date': __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    all_reviews.append(review_data)
                
                print(f"  Found {len(reviews)} reviews")
        
        # Add delay to respect rate limits
        __import__('time').sleep(1)
    
    # Save data
    import pandas as pd
    import os
    
    output_dir = '/content/pokhara_reviews_specific'
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = __import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save reviews
    if all_reviews:
        reviews_df = pd.DataFrame(all_reviews)
        reviews_file = f"{output_dir}/specific_places_reviews_{timestamp}.csv"
        reviews_df.to_csv(reviews_file, index=False, encoding='utf-8-sig')
        print(f"✓ Reviews saved: {reviews_file}")
    
    # Save places
    if all_places:
        places_df = pd.DataFrame(all_places)
        places_file = f"{output_dir}/specific_places_info_{timestamp}.csv"
        places_df.to_csv(places_file, index=False, encoding='utf-8-sig')
        print(f"✓ Places saved: {places_file}")


# =============================================================================
# EXAMPLE 4: ANALYZE EXTRACTED DATA
# =============================================================================

def example_data_analysis():
    """
    Example 4: Analyze extracted review data
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: ANALYZE EXTRACTED DATA")
    print("="*80)
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import os
    import glob
    
    # Find latest extracted files
    output_dir = '/content/pokhara_reviews'
    if not os.path.exists(output_dir):
        print(f"❌ Output directory not found: {output_dir}")
        return
    
    # Get latest files
    review_files = glob.glob(f"{output_dir}/pokhara_reviews_*.csv")
    places_files = glob.glob(f"{output_dir}/pokhara_places_*.csv")
    
    if not review_files or not places_files:
        print("❌ No data files found. Run extraction first.")
        return
    
    # Load latest files
    latest_reviews = max(review_files, key=os.path.getctime)
    latest_places = max(places_files, key=os.path.getctime)
    
    print(f"Loading data from:")
    print(f"  Reviews: {os.path.basename(latest_reviews)}")
    print(f"  Places: {os.path.basename(latest_places)}")
    
    # Load data
    reviews_df = pd.read_csv(latest_reviews)
    places_df = pd.read_csv(latest_places)
    
    print(f"\n{'='*60}")
    print("BASIC STATISTICS")
    print(f"{'='*60}")
    
    # Basic statistics
    print(f"Total places: {len(places_df)}")
    print(f"Total reviews: {len(reviews_df)}")
    print(f"Average rating across all places: {places_df['rating'].mean():.2f}")
    print(f"Average review rating: {reviews_df['rating'].mean():.2f}")
    
    # Reviews by category
    print(f"\n{'='*60}")
    print("REVIEWS BY CATEGORY")
    print(f"{'='*60}")
    category_stats = reviews_df.groupby('place_category').agg({
        'rating': ['count', 'mean'],
        'place_name': 'nunique'
    }).round(2)
    category_stats.columns = ['Review Count', 'Avg Rating', 'Unique Places']
    print(category_stats)
    
    # Top rated places
    print(f"\n{'='*60}")
    print("TOP 10 HIGHEST RATED PLACES")
    print(f"{'='*60}")
    top_rated = places_df.nlargest(10, 'rating')[['name', 'search_category', 'rating', 'total_ratings']]
    print(top_rated.to_string(index=False))
    
    # Most reviewed places
    print(f"\n{'='*60}")
    print("TOP 10 MOST REVIEWED PLACES")
    print(f"{'='*60}")
    most_reviewed = places_df.nlargest(10, 'total_ratings')[['name', 'search_category', 'rating', 'total_ratings']]
    print(most_reviewed.to_string(index=False))
    
    # Sample reviews
    print(f"\n{'='*60}")
    print("SAMPLE REVIEWS")
    print(f"{'='*60}")
    sample_reviews = reviews_df[['place_name', 'place_category', 'rating', 'review_text']].head(5)
    for idx, review in sample_reviews.iterrows():
        print(f"\nPlace: {review['place_name']} ({review['place_category']})")
        print(f"Rating: {review['rating']}/5")
        print(f"Review: {review['review_text'][:200]}...")


# =============================================================================
# EXAMPLE 5: SENTIMENT ANALYSIS
# =============================================================================

def example_sentiment_analysis():
    """
    Example 5: Perform sentiment analysis on extracted reviews
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: SENTIMENT ANALYSIS")
    print("="*80)
    
    import pandas as pd
    from textblob import TextBlob
    import matplotlib.pyplot as plt
    import os
    import glob
    
    # Install textblob if needed
    try:
        from textblob import TextBlob
    except ImportError:
        print("Installing textblob...")
        os.system("pip install textblob")
        from textblob import TextBlob
    
    # Find latest reviews file
    output_dir = '/content/pokhara_reviews'
    review_files = glob.glob(f"{output_dir}/pokhara_reviews_*.csv")
    
    if not review_files:
        print("❌ No review files found. Run extraction first.")
        return
    
    latest_reviews = max(review_files, key=os.path.getctime)
    reviews_df = pd.read_csv(latest_reviews)
    
    print(f"Analyzing sentiment for {len(reviews_df)} reviews...")
    
    # Analyze sentiment
    sentiments = []
    polarity_scores = []
    
    for review in reviews_df['review_text']:
        if pd.notna(review) and review.strip():
            blob = TextBlob(str(review))
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                sentiment = 'Positive'
            elif polarity < -0.1:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'
        else:
            sentiment = 'Neutral'
            polarity = 0
            
        sentiments.append(sentiment)
        polarity_scores.append(polarity)
    
    # Add to dataframe
    reviews_df['sentiment'] = sentiments
    reviews_df['sentiment_polarity'] = polarity_scores
    
    # Display results
    print(f"\n{'='*60}")
    print("SENTIMENT DISTRIBUTION")
    print(f"{'='*60}")
    sentiment_counts = reviews_df['sentiment'].value_counts()
    for sentiment, count in sentiment_counts.items():
        percentage = (count / len(reviews_df)) * 100
        print(f"  {sentiment}: {count} ({percentage:.1f}%)")
    
    # Sentiment by category
    print(f"\n{'='*60}")
    print("SENTIMENT BY CATEGORY")
    print(f"{'='*60}")
    sentiment_by_category = pd.crosstab(reviews_df['place_category'], reviews_df['sentiment'], normalize='index') * 100
    print(sentiment_by_category.round(1))
    
    # Save updated dataset
    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"{output_dir}/pokhara_reviews_with_sentiment_{timestamp}.csv"
    reviews_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✅ Sentiment analysis complete!")
    print(f"Saved to: {output_file}")


# =============================================================================
# EXAMPLE 6: CREATE CUSTOM VISUALIZATIONS
# =============================================================================

def example_custom_visualizations():
    """
    Example 6: Create custom visualizations
    """
    print("\n" + "="*80)
    print("EXAMPLE 6: CUSTOM VISUALIZATIONS")
    print("="*80)
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import os
    import glob
    
    # Find latest files
    output_dir = '/content/pokhara_reviews'
    review_files = glob.glob(f"{output_dir}/pokhara_reviews_*.csv")
    places_files = glob.glob(f"{output_dir}/pokhara_places_*.csv")
    
    if not review_files or not places_files:
        print("❌ No data files found. Run extraction first.")
        return
    
    # Load data
    reviews_df = pd.read_csv(max(review_files, key=os.path.getctime))
    places_df = pd.read_csv(max(places_files, key=os.path.getctime))
    
    # Set style
    sns.set_style("whitegrid")
    
    # Create multiple visualizations
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Pokhara Reviews - Comprehensive Analysis', fontsize=20, fontweight='bold')
    
    # 1. Rating distribution by category
    sns.boxplot(data=reviews_df, x='place_category', y='rating', ax=axes[0, 0])
    axes[0, 0].set_title('Rating Distribution by Category', fontweight='bold')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # 2. Number of reviews over time (if timestamp available)
    if 'review_timestamp' in reviews_df.columns:
        reviews_df['review_date'] = pd.to_datetime(reviews_df['review_timestamp'], unit='s', errors='coerce')
        reviews_by_month = reviews_df.groupby(reviews_df['review_date'].dt.to_period('M')).size()
        reviews_by_month.plot(kind='line', ax=axes[0, 1], marker='o')
        axes[0, 1].set_title('Reviews Over Time', fontweight='bold')
        axes[0, 1].set_ylabel('Number of Reviews')
    else:
        axes[0, 1].text(0.5, 0.5, 'Timestamp data not available', ha='center', va='center', transform=axes[0, 1].transAxes)
        axes[0, 1].set_title('Reviews Over Time', fontweight='bold')
    
    # 3. Average rating vs total ratings
    scatter_data = places_df[places_df['total_ratings'] > 0]
    axes[0, 2].scatter(scatter_data['total_ratings'], scatter_data['rating'], alpha=0.6)
    axes[0, 2].set_xlabel('Total Ratings')
    axes[0, 2].set_ylabel('Average Rating')
    axes[0, 2].set_title('Rating vs Popularity', fontweight='bold')
    axes[0, 2].set_xscale('log')
    
    # 4. Top 10 most reviewed places
    top_reviewed = places_df.nlargest(10, 'total_ratings')
    axes[1, 0].barh(range(len(top_reviewed)), top_reviewed['total_ratings'])
    axes[1, 0].set_yticks(range(len(top_reviewed)))
    axes[1, 0].set_yticklabels(top_reviewed['name'], fontsize=8)
    axes[1, 0].set_xlabel('Total Ratings')
    axes[1, 0].set_title('Top 10 Most Reviewed Places', fontweight='bold')
    
    # 5. Rating distribution
    axes[1, 1].hist(reviews_df['rating'], bins=5, edgecolor='black', alpha=0.7, color='lightcoral')
    axes[1, 1].set_xlabel('Rating')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].set_title('Overall Rating Distribution', fontweight='bold')
    axes[1, 1].set_xticks([1, 2, 3, 4, 5])
    
    # 6. Places count by category
    category_counts = places_df['search_category'].value_counts()
    axes[1, 2].pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
    axes[1, 2].set_title('Places Distribution by Category', fontweight='bold')
    
    plt.tight_layout()
    
    # Save visualization
    viz_file = f"{output_dir}/custom_visualizations.png"
    plt.savefig(viz_file, dpi=300, bbox_inches='tight')
    print(f"✅ Custom visualizations saved to: {viz_file}")
    
    plt.show()


# =============================================================================
# EXAMPLE 7: EXPORT TO DIFFERENT FORMATS
# =============================================================================

def example_export_formats():
    """
    Example 7: Export data to different formats
    """
    print("\n" + "="*80)
    print("EXAMPLE 7: EXPORT TO DIFFERENT FORMATS")
    print("="*80)
    
    import pandas as pd
    import os
    import glob
    
    # Find latest files
    output_dir = '/content/pokhara_reviews'
    review_files = glob.glob(f"{output_dir}/pokhara_reviews_*.csv")
    places_files = glob.glob(f"{output_dir}/pokhara_places_*.csv")
    
    if not review_files or not places_files:
        print("❌ No data files found. Run extraction first.")
        return
    
    # Load data
    reviews_df = pd.read_csv(max(review_files, key=os.path.getctime))
    places_df = pd.read_csv(max(places_files, key=os.path.getctime))
    
    # Create export directory
    export_dir = '/content/pokhara_reviews_exports'
    os.makedirs(export_dir, exist_ok=True)
    
    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
    
    # Export to Excel
    print("Exporting to Excel...")
    excel_file = f"{export_dir}/pokhara_reviews_{timestamp}.xlsx"
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        reviews_df.to_excel(writer, sheet_name='Reviews', index=False)
        places_df.to_excel(writer, sheet_name='Places', index=False)
    print(f"✓ Excel file saved: {excel_file}")
    
    # Export to JSON
    print("Exporting to JSON...")
    json_file = f"{export_dir}/pokhara_reviews_{timestamp}.json"
    
    # Combine data
    combined_data = {
        'extraction_date': timestamp,
        'total_places': len(places_df),
        'total_reviews': len(reviews_df),
        'places': places_df.to_dict('records'),
        'reviews': reviews_df.to_dict('records')
    }
    
    import json
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, indent=2, ensure_ascii=False)
    print(f"✓ JSON file saved: {json_file}")
    
    # Export filtered data (highly rated places only)
    print("Exporting filtered data (highly rated places)...")
    highly_rated_places = places_df[places_df['rating'] >= 4.5]
    highly_rated_reviews = reviews_df[reviews_df['place_id'].isin(highly_rated_places['place_id'])]
    
    filtered_excel = f"{export_dir}/pokhara_highly_rated_{timestamp}.xlsx"
    with pd.ExcelWriter(filtered_excel, engine='openpyxl') as writer:
        highly_rated_reviews.to_excel(writer, sheet_name='Reviews', index=False)
        highly_rated_places.to_excel(writer, sheet_name='Places', index=False)
    print(f"✓ Filtered Excel file saved: {filtered_excel}")
    
    # Export to SQLite database
    print("Exporting to SQLite database...")
    sqlite_file = f"{export_dir}/pokhara_reviews_{timestamp}.db"
    import sqlite3
    conn = sqlite3.connect(sqlite_file)
    reviews_df.to_sql('reviews', conn, if_exists='replace', index=False)
    places_df.to_sql('places', conn, if_exists='replace', index=False)
    conn.close()
    print(f"✓ SQLite database saved: {sqlite_file}")
    
    print(f"\n✅ All exports complete! Files saved in: {export_dir}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    """
    Run examples based on user choice
    """
    print("="*80)
    print("POKHARA GOOGLE REVIEWS SCRAPER - EXAMPLES")
    print("="*80)
    print("\nChoose an example to run:")
    print("1. Basic usage - Extract all reviews")
    print("2. Specific categories only")
    print("3. Specific places only")
    print("4. Analyze extracted data")
    print("5. Sentiment analysis")
    print("6. Custom visualizations")
    print("7. Export to different formats")
    print("8. Run all examples")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-8): ").strip()
    
    examples = {
        '1': example_basic_usage,
        '2': example_specific_categories,
        '3': example_specific_places,
        '4': example_data_analysis,
        '5': example_sentiment_analysis,
        '6': example_custom_visualizations,
        '7': example_export_formats,
    }
    
    if choice == '8':
        # Run all examples
        for example_func in examples.values():
            try:
                example_func()
            except Exception as e:
                print(f"❌ Error in example: {e}")
    elif choice in examples:
        # Run specific example
        try:
            examples[choice]()
        except Exception as e:
            print(f"❌ Error: {e}")
    elif choice == '0':
        print("Goodbye!")
    else:
        print("❌ Invalid choice. Please run the script again.")

"""
ADDITIONAL TIPS AND TRICKS:
==========================

1. BATCH PROCESSING:
   If you have a large list of places, process them in batches:
   
   places_list = [...]  # Your long list
   batch_size = 10
   
   for i in range(0, len(places_list), batch_size):
       batch = places_list[i:i+batch_size]
       # Process batch
       time.sleep(60)  # Wait 1 minute between batches

2. ERROR HANDLING:
   Always wrap API calls in try-except blocks:
   
   try:
       results = client.search_places_nearby(...)
   except Exception as e:
       print(f"Error: {e}")
       # Handle error or retry

3. CACHING:
   Cache results to avoid repeated API calls:
   
   import pickle
   
   # Save results
   with open('cached_results.pkl', 'wb') as f:
       pickle.dump(results, f)
   
   # Load results
   with open('cached_results.pkl', 'rb') as f:
       results = pickle.load(f)

4. PROXY SETTINGS:
   If you're behind a proxy, configure it:
   
   import os
   os.environ['HTTP_PROXY'] = 'http://proxy.example.com:8080'
   os.environ['HTTPS_PROXY'] = 'https://proxy.example.com:8080'

5. LOGGING:
   Enable detailed logging for debugging:
   
   import logging
   logging.basicConfig(level=logging.DEBUG)
   
6. PARALLEL PROCESSING:
   For faster processing (respect rate limits!):
   
   from concurrent.futures import ThreadPoolExecutor
   
   with ThreadPoolExecutor(max_workers=2) as executor:
       futures = [executor.submit(process_place, place) for place in places]
       for future in futures:
           result = future.result()

7. DATA VALIDATION:
   Always validate extracted data:
   
   # Check for missing values
   print(reviews_df.isnull().sum())
   
   # Check data types
   print(reviews_df.dtypes)
   
   # Remove duplicates
   reviews_df = reviews_df.drop_duplicates()

8. BACKUP STRATEGY:
   Always backup your API key and configuration:
   
   # Store in environment variable
   export GOOGLE_API_KEY="your_key_here"
   
   # Or use config file
   from configparser import ConfigParser
   config = ConfigParser()
   config.read('secrets.ini')
   api_key = config['google']['api_key']

9. MONITORING:
   Track your API usage:
   
   import requests
   
   def check_api_quota():
       url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id=...&key={GOOGLE_API_KEY}"
       response = requests.get(url)
       # Check response headers for quota information
       print(response.headers)

10. TESTING:
    Test with small dataset first:
    
    # Test with just 5 places
    extractor.extract_all_reviews(max_places_per_category=5)
    
    # If successful, run with larger dataset
    extractor.extract_all_reviews(max_places_per_category=50)
"""
