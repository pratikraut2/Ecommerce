import os
import requests
import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import urllib.request

def setup_driver():
    """Setup Chrome driver with better anti-detection"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Execute script to remove webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def download_image(url, filename):
    """Download image from URL and save to media/products/"""
    if not url or "data:image" in url:
        return None
    
    try:
        # Create media/products directory if it doesn't exist
        os.makedirs('media/products', exist_ok=True)
        
        # Full path for saving
        filepath = os.path.join('media', 'products', filename)
        
        # Download image with better error handling
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
        # Use requests instead of urllib for better handling
        response = requests.get(url, headers=headers, timeout=10, stream=True)
        response.raise_for_status()
        
        # Check if it's actually an image
        content_type = response.headers.get('content-type', '')
        if 'image' not in content_type.lower():
            print(f"❌ Not an image: {content_type}")
            return None
            
        # Save the image
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Verify file was created and has content
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            return f"products/{filename}"
        else:
            return None
        
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return None

def create_placeholder_image(filename, product_name):
    """Create a simple placeholder image if download fails"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create media/products directory if it doesn't exist
        os.makedirs('media/products', exist_ok=True)
        
        filepath = os.path.join('media', 'products', filename)
        
        # Create a simple image
        img = Image.new('RGB', (300, 300), color=(70, 130, 180))
        draw = ImageDraw.Draw(img)
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Wrap text if too long
        if len(product_name) > 20:
            product_name = product_name[:17] + "..."
        
        bbox = draw.textbbox((0, 0), product_name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (300 - text_width) // 2
        y = (300 - text_height) // 2
        
        draw.text((x, y), product_name, fill='white', font=font)
        
        # Save the image
        img.save(filepath, 'JPEG', quality=85)
        return True
        
    except ImportError:
        # If PIL not available, create a simple text file as placeholder
        filepath = os.path.join('media', 'products', filename.replace('.jpg', '.txt'))
        with open(filepath, 'w') as f:
            f.write(f"Placeholder for {product_name}")
        return True
    except Exception as e:
        print(f"❌ Failed to create placeholder: {e}")
        return False

def get_product_data(container, product_index):
    """Extract product data with multiple selector fallbacks"""
    product_data = {}
    
    # Product name - try multiple selectors
    name_selectors = [
        "h2 a span",
        "[data-cy='title-recipe-title']",
        "h2 span",
        ".a-size-mini span",
        ".a-size-base-plus",
        ".s-size-mini"
    ]
    
    name = ""
    for selector in name_selectors:
        try:
            elem = container.find_element(By.CSS_SELECTOR, selector)
            name = elem.text.strip()
            if name and len(name) > 5:  # Valid name found
                break
        except:
            continue
    
    if not name:
        return None
    
    product_data['name'] = name[:200]
    
    # Price - try multiple selectors
    price_selectors = [
        ".a-price-whole",
        ".a-price .a-offscreen",
        ".a-price-range .a-price .a-offscreen",
        "[data-a-color='price'] .a-offscreen"
    ]
    
    price = "0.00"
    for selector in price_selectors:
        try:
            elem = container.find_element(By.CSS_SELECTOR, selector)
            price_text = elem.get_attribute("textContent") or elem.text
            price = ''.join(c for c in price_text if c.isdigit() or c == '.')
            if price and float(price) > 0:
                break
        except:
            continue
    
    product_data['price'] = price or "0.00"
    
    # Rating
    rating = "4.0"  # Default rating
    rating_selectors = [
        ".a-icon-alt",
        "[data-cy='reviews-ratings-slot'] .a-icon-alt",
        ".a-icon-row .a-icon-alt"
    ]
    
    for selector in rating_selectors:
        try:
            elem = container.find_element(By.CSS_SELECTOR, selector)
            rating_text = elem.get_attribute("textContent")
            if rating_text and "out of" in rating_text:
                rating = rating_text.split()[0]
                break
        except:
            continue
    
    product_data['rating'] = rating
    
    # Image URL and Download
    image_selectors = [
        "img",
        ".s-image",
        "[data-component-type='s-product-image'] img"
    ]
    
    image_url = ""
    for selector in image_selectors:
        try:
            img_elem = container.find_element(By.CSS_SELECTOR, selector)
            image_url = img_elem.get_attribute("src")
            if image_url and "data:image" not in image_url:
                break
        except:
            continue
    
    # Download the image
    if image_url:
        # Get file extension from URL
        parsed_url = urlparse(image_url)
        ext = '.jpg'  # Default extension
        if '.' in parsed_url.path:
            ext = os.path.splitext(parsed_url.path)[1][:4]  # Limit extension length
        
        filename = f"mobile_{product_index}{ext}"
        downloaded_path = download_image(image_url, filename)
        product_data['image'] = downloaded_path or f"products/{filename}"
    else:
        product_data['image'] = f"products/mobile_{product_index}.jpg"
    
    product_data['image_url'] = image_url
    
    return product_data

def scrape_with_image_download():
    """Scrape Amazon with image download"""
    URL = "https://www.amazon.in/s?k=mobile+phone&ref=nb_sb_noss"
    
    driver = setup_driver()
    products = []
    
    try:
        print("Loading Amazon page...")
        driver.get(URL)
        time.sleep(5)  # Wait for page to load
        
        # Wait for products to load
        wait = WebDriverWait(driver, 15)
        
        # Try different container selectors
        container_selectors = [
            "[data-component-type='s-search-result']",
            ".s-result-item",
            "[data-asin]:not([data-asin=''])"
        ]
        
        containers = []
        for selector in container_selectors:
            try:
                containers = driver.find_elements(By.CSS_SELECTOR, selector)
                if containers:
                    print(f"Found {len(containers)} products using selector: {selector}")
                    break
            except:
                continue
        
        if not containers:
            print("No product containers found!")
            return []
        
        # Extract product data
        for i, container in enumerate(containers[:10]):  # Limit to 10 products
            print(f"\nProcessing product {i+1}...")
            
            product_data = get_product_data(container, i+1)
            if product_data:
                # Add additional fields
                product_data.update({
                    'brand': 'Unknown',
                    'category__name': 'Mobile',
                    'description': f"{product_data['name']} - Mobile phone",
                    'stock': random.randint(5, 50),
                    'is_active': True
                })
                
                products.append(product_data)
                print(f"✅ {product_data['name'][:50]}... - ₹{product_data['price']}")
            else:
                print(f"❌ Could not extract data for product {i+1}")
            
            time.sleep(random.uniform(1, 2))
    
    except Exception as e:
        print(f"Error during scraping: {e}")
    
    finally:
        driver.quit()
    
    return products

# Alternative: Create sample images if scraping fails
def create_sample_images():
    """Create placeholder images for testing"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        os.makedirs('media/products', exist_ok=True)
        
        for i in range(1, 11):
            # Create a simple colored rectangle as placeholder
            img = Image.new('RGB', (300, 300), color=(70, 130, 180))
            draw = ImageDraw.Draw(img)
            
            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 36)
            except:
                font = ImageFont.load_default()
            
            text = f"Mobile {i}"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (300 - text_width) // 2
            y = (300 - text_height) // 2
            
            draw.text((x, y), text, fill='white', font=font)
            
            filename = f"mobile_{i}.jpg"
            filepath = os.path.join('media', 'products', filename)
            img.save(filepath)
            
        print("✅ Created 10 placeholder images")
        return True
        
    except ImportError:
        print("❌ PIL not installed. Install it with: pip install Pillow")
        return False

if __name__ == "__main__":
    print("🛒 Amazon Scraper with Image Download")
    print("=" * 50)
    
    products = scrape_with_image_download()
    
    if products:
        df = pd.DataFrame(products)
        df.to_csv('products_scraped_fixed.csv', index=False)
        print(f"\n✅ Scraped {len(products)} products successfully!")
        print("💾 Saved to products_scraped_fixed.csv")
        print("🖼️ Images downloaded to media/products/")
    else:
        print("❌ No products were scraped. Creating sample images instead...")
        if create_sample_images():
            # Create sample CSV data
            sample_data = []
            for i in range(1, 11):
                sample_data.append({
                    'name': f'Sample Mobile Phone {i}',
                    'brand': 'SampleBrand',
                    'category__name': 'Mobile',
                    'description': f'Sample mobile phone {i} description',
                    'price': random.uniform(10000, 50000),
                    'stock': random.randint(5, 50),
                    'image': f'products/mobile_{i}.jpg',
                    'rating': round(random.uniform(3.5, 5.0), 1),
                    'is_active': True
                })
            
            df = pd.DataFrame(sample_data)
            df.to_csv('products_scraped_fixed.csv', index=False)
            print("✅ Created sample data with images!")