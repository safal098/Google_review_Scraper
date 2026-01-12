"""
Google Reviews Scraper for Pokhara City - Selenium Version (No API Key)
====================================================================
This script extracts reviews for places, hotels, lakes, and viewpoints around Pokhara
using Selenium web scraping. It uses specific locations defined in config.py.

Author: AI Assistant
Date: 2026-01-01
"""

import time
import re
import os
import pandas as pd
from datetime import datetime
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Import existing configuration
try:
    import config
except ImportError:
    # If running from within Scraper directory
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import config

class GoogleMapsSeleniumScraper:
    """Scraper using Selenium to extract reviews from Google Maps without API key"""
    
    def __init__(self, output_dir='pokhara_reviews'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.driver = None
        self.all_reviews = []
        self.places_data = []

    def setup_driver(self):
        """Set up Chrome WebDriver"""
        chrome_options = Options()
        
        # Add options from config
        if hasattr(config, 'CHROME_OPTIONS'):
            for option in config.CHROME_OPTIONS:
                chrome_options.add_argument(option)
        else:
            # Fallback defaults if config is missing options
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--lang=en-US')
            
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # You can add --headless here if you don't want to see the browser
        # chrome_options.add_argument('--headless')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✓ Chrome WebDriver ready!")

    def search_and_navigate(self, query):
        """Search for a place and navigate to its reviews"""
        print(f"\nSearching for: {query}")
        self.driver.get(f"https://www.google.com/maps/search/{query}?hl=en")
        time.sleep(5)
        
        # Check if we landed on a specific place or a list
        try:
            # Wait for either a result link or the place details header
            print("Waiting for search results...")
            WebDriverWait(self.driver, 10).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, "a.hfpxzc") or 
                          d.find_elements(By.CSS_SELECTOR, "h1.DUwDvf")
            )
            
            # If we see a list of results (links with class hfpxzc), click the first one
            results = self.driver.find_elements(By.CSS_SELECTOR, "a.hfpxzc")
            if results:
                print(f"Found {len(results)} results, clicking the first one...")
                try:
                    self.driver.execute_script("arguments[0].click();", results[0])
                    time.sleep(5) # Wait for details to slide in
                except Exception as e:
                    print(f"Could not click result: {e}")
            else:
                print("Appears to be a direct place match.")
                
        except Exception as e:
            print(f"Search navigation warning: {e}")

        # Try to find the "Reviews" tab
        try:
            # Try multiple selectors for the reviews tab/button
            # Prioritize Nepali since environment defaults to it
            review_selectors = [
                "button[aria-label*='समीक्षाहरु']",      # Nepali: Reviews
                "button[aria-label*='Reviews']",         # English
                "div[role='tablist'] button:nth-child(2)", # Index based
                "//button[contains(@aria-label, 'समीक्षा')]", # XPath fallback
                "//button[contains(@aria-label, 'Reviews')]"  # XPath fallback
            ]
            
            for selector in review_selectors:
                try:
                    if selector.startswith("//"):
                        reviews_tab = self.driver.find_element(By.XPATH, selector)
                    else:
                        reviews_tab = self.driver.find_element(By.CSS_SELECTOR, selector)
                    reviews_tab.click()
                    print("✓ Navigated to Reviews tab")
                    
                    # Wait for reviews to load
                    print("Waiting for reviews to appear...")
                    start_wait = time.time()
                    while time.time() - start_wait < 20:
                        if len(self.driver.find_elements(By.CSS_SELECTOR, "div.jftiEf")) > 0:
                            print("✓ Reviews section loaded!")
                            time.sleep(2)
                            return True
                        time.sleep(1)
                    print(f"⚠ Reviews loaded check timed out for selector '{selector}'")
                    continue # Try next selector
                except Exception as e:
                    # print(f"DEBUG: Failed selector {selector}: {e}")
                    continue
            
            print("⚠ All review selectors failed or reviews did not load.")
            return False
            
            # If tab not found, maybe it's already visible or under a different selector
            if len(self.driver.find_elements(By.CSS_SELECTOR, "div.jftiEf")) > 0:
                print("✓ Reviews already visible")
                return True
                
        except Exception as e:
            print(f"⚠ Could not navigate to reviews tab: {e}")
            
        return False

    def scroll_reviews(self, max_reviews=50):
        """Scroll to load reviews up to max_reviews"""
        print(f"Scrolling to load up to {max_reviews} reviews...")
        
        scroll_script = """
        var scrollableDiv = document.querySelector('div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde') || 
                             document.querySelector('div[role="main"]') ||
                             document.querySelector('div[tabindex="-1"]');
                             
        // Fallback: Try to find ANY div that is scrollable
        if (!scrollableDiv) {
            var allDivs = document.getElementsByTagName('div');
            for (var i = 0; i < allDivs.length; i++) {
                var div = allDivs[i];
                if (div.scrollHeight > div.clientHeight && div.clientHeight > 0) {
                    scrollableDiv = div;
                    break;
                }
            }
        }

        if (scrollableDiv) {
            scrollableDiv.scrollTop = scrollableDiv.scrollHeight;
            return scrollableDiv.scrollHeight;
        }
        return 0;
        """
        
        count_script = "return document.querySelectorAll('div.jftiEf').length;"
        
        no_change_count = 0
        last_count = 0
        scroll_num = 0
        
        while True:
            self.driver.execute_script(scroll_script)
            time.sleep(2)
            
            current_count = self.driver.execute_script(count_script)
            scroll_num += 1
            
            if current_count >= max_reviews:
                print(f"Loaded {current_count} reviews.")
                break
                
            if current_count == last_count:
                no_change_count += 1
            else:
                no_change_count = 0
                
            if no_change_count >= 5:
                print(f"Reached end of reviews or stuck. Loaded {current_count}.")
                break
                
            last_count = current_count
            if scroll_num > 50: # Safety break
                break

    def sort_reviews_by_newest(self):
        """Click 'Sort' and select 'Newest' to get all languages"""
        try:
            print("Attempting to sort by Newest...")
            # Valid selectors for Sort button (English and Nepali and generic)
            sort_selectors = [
                "button[aria-label='Sort reviews']", 
                "button[aria-label*='क्रमबद्ध']", # Nepali: Sort
                "button[data-value='Sort']",
                "//button[contains(@aria-label, 'Sort')]",
                "//button[contains(@aria-label, 'क्रमबद्ध')]"
            ]
            
            sort_btn = None
            for sel in sort_selectors:
                try:
                    if sel.startswith("//"):
                        sort_btn = self.driver.find_element(By.XPATH, sel)
                    else:
                        sort_btn = self.driver.find_element(By.CSS_SELECTOR, sel)
                    if sort_btn:
                        break
                except:
                    continue
            
            if sort_btn:
                self.driver.execute_script("arguments[0].click();", sort_btn)
                time.sleep(1)
                
                # Click 'Newest' option (usually the second item in menu)
                # English: "Newest", Nepali: "नयाँ" or similar
                # Best to use index/generic selector for the menu item
                menu_items = self.driver.find_elements(By.CSS_SELECTOR, "div[role='menuitemradio']")
                if len(menu_items) >= 2:
                    print("Clicking 'Newest' option...")
                    self.driver.execute_script("arguments[0].click();", menu_items[1]) 
                    time.sleep(2)
                else:
                    print("Could not find Newest option in menu")
            else:
                print("Could not find Sort button")
        except Exception as e:
            print(f"Sort by newest failed: {e}")

    def expand_more_buttons(self):
        """Expand 'More' buttons in reviews"""
        expand_script = """
        var buttons = document.querySelectorAll('button.w8B4Bf');
        buttons.forEach(function(btn) {
            try { btn.click(); } catch(e) {}
        });
        """
        self.driver.execute_script(expand_script)
        time.sleep(1)

    def is_code_switched(self, text):
        """Detect Nepali-English code-switching (Devanagari mixed or Romanized mixed)"""
        if not text:
            return False
            
        text_lower = text.lower()
        
        # 1. Devanagari detection
        has_nepali_script = bool(re.search(r'[\u0900-\u097F]', text))
        has_english_script = bool(re.search(r'[a-zA-Z]', text))
        
        if has_nepali_script and has_english_script:
            # print(f"DEBUG: Found Devanagari CS: {text[:30]}...")
            return True
            
        # 2. Romanized Nepali detection (English script + Nepali keywords)
        # Common romanized keywords
        nepali_keywords = [
            'ramro', 'dherai', 'kati', 'chha', 'ho', 'ni', 
            'dammi', 'babal', 'thik', 'gardai', 'parne', 'hola',
            'sarai', 'ekdam', 'yo', 'ta', 'pani', 'ma', 'gardai',
            'haina', 'huna', 'garne', 'hun', 'kati', 'kasto'
        ]
        
        # Check if keywords appear in text (whole words only)
        words = set(re.findall(r'\b\w+\b', text_lower))
        has_nepali_keyword = any(kw in words for kw in nepali_keywords)
        
        if has_english_script and has_nepali_keyword:
            # print(f"DEBUG: Found Romanized CS: {text[:30]}...")
            return True
            
        return False

    def extract_visible_reviews(self, place_name, category):
        """Extract all currently loaded reviews"""
        review_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.jftiEf")
        extracted = []
        
        for elem in review_elements:
            try:
                # Reviewer name
                try:
                    name = elem.find_element(By.CSS_SELECTOR, "div.d4r55").text
                except:
                    name = "Anonymous"
                
                # Rating
                try:
                    rating_elem = elem.find_element(By.CSS_SELECTOR, "span.kvMYJc")
                    rating_aria = rating_elem.get_attribute("aria-label")
                    rating_match = re.search(r'(\d+)', rating_aria)
                    rating = int(rating_match.group(1)) if rating_match else 0
                except:
                    rating = 0
                
                # Date
                try:
                    date = elem.find_element(By.CSS_SELECTOR, "span.rsqaWe").text
                except:
                    date = "Unknown"
                
                # Review text
                try:
                    text = elem.find_element(By.CSS_SELECTOR, "span.wiI7pd").text
                except:
                    text = ""
                
                is_cs = self.is_code_switched(text)
                
                extracted.append({
                    'place_name': place_name,
                    'category': category,
                    'reviewer_name': name,
                    'rating': rating,
                    'review_date': date,
                    'review_text': text,
                    'is_code_switched': is_cs,
                    'extraction_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            except Exception as e:
                continue
        
        return extracted

    def scrape_all_from_config(self):
        """Iterate through config and scrape everything"""
        self.setup_driver()
        
        try:
            for category, names in config.SPECIFIC_PLACES.items():
                print(f"\n--- Scraping Category: {category} ---")
                for name in names:
                    try:
                        query = f"{name} Pokhara"
                        if self.search_and_navigate(query):
                            # Get place details if needed (simplified here)
                            self.places_data.append({
                                'name': name,
                                'category': category,
                                'query': query,
                                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                            
                            # Sort by newest to get mixed languages
                            self.sort_reviews_by_newest()
                            
                            self.scroll_reviews(max_reviews=config.WEB_SCRAPE_MAX_REVIEWS)
                            self.expand_more_buttons()
                            reviews = self.extract_visible_reviews(name, category)
                            print(f"Extracted {len(reviews)} reviews for {name}")
                            
                            if len(reviews) == 0:
                                print("⚠ No reviews extracted! Saving page source for debugging...")
                                with open(os.path.join(self.output_dir, "debug_page_source.html"), "w", encoding="utf-8") as f:
                                    f.write(self.driver.page_source)
                                print(f"✓ Saved page source to {os.path.join(self.output_dir, 'debug_page_source.html')}")
                            
                            self.all_reviews.extend(reviews)
                            
                            # Interval save to prevent data loss
                            self.save_data(interim=True)
                        else:
                            print(f"❌ Failed to find reviews for {name}")
                    except Exception as e:
                        print(f"⚠ Error scraping {name}: {e}")
                        continue
        
        except KeyboardInterrupt:
            print("\n\n⚠ SCRAPING INTERRUPTED BY USER (Ctrl+C)")
            print("Saving collected data before exiting...")
            self.save_data(interim=True)
            print("✓ Data saved safely.")
            
        finally:
            if self.driver:
                self.driver.quit()
            self.save_data()

    def save_data(self, interim=False):
        """Save reviews and places data to CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        suffix = "_interim" if interim else ""
        
        if self.all_reviews:
            df = pd.DataFrame(self.all_reviews)
            # Save ALL reviews to main file
            # Note: This includes English, Nepali, and Code-switched reviews
            df = df.drop_duplicates(subset=['place_name', 'reviewer_name', 'review_text'])
            reviews_file = os.path.join(self.output_dir, f"pokhara_reviews{suffix}.csv")
            df.to_csv(reviews_file, index=False, encoding='utf-8-sig')
            
            # Save code-switched separately (as a subset, for convenience)
            cs_df = df[df['is_code_switched'] == True]
            if not cs_df.empty:
                cs_file = os.path.join(self.output_dir, f"pokhara_reviews_code_switched{suffix}.csv")
                cs_df.to_csv(cs_file, index=False, encoding='utf-8-sig')

        if self.places_data:
            df_places = pd.DataFrame(self.places_data)
            places_file = os.path.join(self.output_dir, f"pokhara_places{suffix}.csv")
            df_places.to_csv(places_file, index=False, encoding='utf-8-sig')

def main():
    print("="*80)
    print("POKHARA GOOGLE REVIEWS SELENIUM SCRAPER")
    print("="*80)
    
    scraper = GoogleMapsSeleniumScraper(output_dir='D:\\Research work\\data\\output_reviews')
    scraper.scrape_all_from_config()
    
    print("\n✅ SCRAPING PROCESS COMPLETED!")

if __name__ == "__main__":
    main()
