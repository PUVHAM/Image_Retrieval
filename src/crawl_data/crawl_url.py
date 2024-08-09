import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class UrlScraper:
    # Constructor
    def __init__(self, url_template, max_images=50, max_workers=4):
        self.url_template = url_template # link crawl
        self.max_images = max_images # max images
        self.max_workers = max_workers # threads
        self.setup_environment()
    
    def setup_environment(self):
        os.environ['PATH'] += ':/usr/lib/chromium-browser'
        os.environ['PATH'] += ':/usr/lib/chromium-browser/chromedriver'

    
    def _replace_image_suffix(self, img_path):
        LARGE_IMAGE_SUFFIX = "_b.jpg"
        return img_path.replace("_m.jpg", LARGE_IMAGE_SUFFIX)\
                       .replace("_n.jpg", LARGE_IMAGE_SUFFIX)\
                       .replace("_w.jpg", LARGE_IMAGE_SUFFIX)

    def _extract_image_urls(self, img_tags, url, urls, pbar):
        for img in img_tags:
            if len(urls) >= self.max_images:
                break
            if 'src' in img.attrs:
                href = img.attrs['src']
                img_path = urljoin(url, href)
                img_path = self._replace_image_suffix(img_path)
                if img_path == "https://combo.staticflickr.com/ap/build/images/getty/IStock_corporate_logo.svg":
                    continue
                urls.append(img_path)
                pbar.update(1)

    def get_url_images(self, term):
        """
        Crawl the urls of images by term

        Parameters:
        term (str): The name of animal, plant, scenery, furniture

        Returns:
        urls (list): List of urls of images
        """
        # Initialize Chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

        url = self.url_template.format(search_term=term)
        driver.get(url)
        
        # Start crawl urls of image like brute force - the same mechanism with this but add some feature
        urls = []
        more_content_available = True

        pbar = tqdm(total=self.max_images, desc=f"Fetching images for {term}") # Set up for visualize progress
        
        while len(urls) < self.max_images and more_content_available:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            img_tags = soup.find_all("img")
            self._extract_image_urls(img_tags, url, urls, pbar)
            
            try:
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,'//button[@id="yui_3_16_0_1_1721642285931_28620"]'))
                )
                load_more_button.click()
                time.sleep(2)
            except Exception:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                new_soup = BeautifulSoup(driver.page_source, "html.parser")
                new_img_tags = new_soup.find_all("img", loading_="lazy")
                if len(new_img_tags) == len(img_tags):
                    more_content_available = False
                img_tags = new_img_tags
                    
        pbar.close()
        driver.quit()
        return urls
    
    def scrape_urls(self, categories):
        all_urls = {category: {} for category in categories}

        # Handle multi-threading for efficent installation
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_term = {executor.submit(self.get_url_images, term): (category, term)
                              for category, terms in categories.items() for term in terms}

            for future in tqdm(as_completed(future_to_term), total=len(future_to_term), desc="Overall Progress"):
                category, term = future_to_term[future]
                try:
                    urls = future.result()
                    all_urls[category][term] = urls
                    print(f"\nNumber of images retrieved for {term}: {len(urls)}")
                except Exception as exc:
                    print(f"\n{term} generated an exception: {exc}")
        return all_urls
    
    def save_to_file(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}")
    
if __name__ == "__main__":
    categories = {
        "animal": ["Monkey", "Elephant", "cows", "Cat", "Dog", "bear", "fox", "Civet", "Pangolins", "Rabbit", "Bats", "Whale", "Cock", "Owl", "flamingo", "Lizard", "Turtle", "Snake", "Frog", "Fish", "shrimp", "Crab", "Snail", "Coral", "Jellyfish", "Butterfly", "Flies", "Mosquito", "Ants", "Cockroaches", "Spider", "scorpion", "tiger", "bird", "horse", "pig", "Alligator", "Alpaca", "Anteater", "donkey", "Bee", "Buffalo", "Camel", "Caterpillar", "Cheetah", "Chicken", "Dragonfly", "Duck", "panda", "Giraffe"],
        "plant": ["Bamboo", "Apple", "Apricot", "Banana", "Bean", "Wildflower", "Flower","Mushroom", "Weed", "Fern", "Reed", "Shrub", "Moss", "Grass", "Palmtree", "Corn", "Tulip", "Rose", "Clove", "Dogwood", "Durian", "Ferns", "Fig", "Flax", "Frangipani", "Lantana", "Hibiscus", "Bougainvillea", "Pea", "OrchidTree", "RangoonCreeper", "Jackfruit", "Cottonplant", "Corneliantree", "Coffeeplant", "Coconut", "wheat", "watermelon", "radish", "carrot"],
        "furniture": ["bed", "cabinet", "chair", "chests", "clock", "desks", "table", "Piano", "Bookcase", "Umbrella", "Clothes", "cart", "sofa", "ball", "spoon", "Bowl", "fridge", "pan", "book"],
        "scenery": ["Cliff", "Bay", "Coast", "Mountains", "Forests", "Waterbodies", "Lake", "desert", "farmland", "river", "hedges", "plain", "sky", "cave", "cloud", "flowergarden", "glacier", "grassland", "horizon", "lighthouse", "plateau", "savannah", "valley", "volcano", "waterfall"]
    }   
    urltopic = {"flickr": "https://www.flickr.com/search/?text={search_term}"}
    scraper = UrlScraper(url_template=urltopic["flickr"], max_images=20, max_workers=5)
    image_urls = scraper.scrape_urls(categories)
    scraper.save_to_file(image_urls, 'image_urls.json')