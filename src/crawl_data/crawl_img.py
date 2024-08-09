import os
import json
import time
from tqdm import tqdm
from urllib.request import urlopen, urlretrieve
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

class ImageDownloader:
    def __init__(self, json_file, download_dir='Dataset', max_workers=4, delay=1):
        self.json_file = json_file
        self.download_dir = download_dir
        self.max_workers = max_workers
        self.delay = delay
        self.filename = set()
        self.setup_directory()
        
    def setup_directory(self):
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            
    def read_json(self):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
        return data
    
    def is_valid_url(self, url):
        try:
            with urlopen(url) as response:
                if response.status == 200 and 'image' in response.info().get_content_type():
                    return True
        except Exception:
            return False

    def download_image(self, url, category, term, pbar):
        if not self.is_valid_url(url):
            pbar.update(1)
            return f"Invalid URL: {url}"
        
        category_dir = os.path.join(self.download_dir, category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
            
        term_dir = os.path.join(category_dir, term)
        if not os.path.exists(term_dir):
            os.makedirs(term_dir)
            
        filename = os.path.join(term_dir, os.path.basename(urlparse(url).path))
        
        self.filename.add(filename)
        
        try:
            urlretrieve(url, filename)
            pbar.update(1)
            return f"Downloaded: {url}"
        except Exception as e:
            pbar.update(1)
            return f"Failed to download {url}: {str(e)}"
        
    def download_images(self):
        data = self.read_json()
        download_tasks = []
        
        total_images = sum(len(urls) for terms in data.values() for urls in terms.values())
        with tqdm(total=total_images, desc="Downloading images") as pbar:
            with ThreadPoolExecutor(max_workers=self.max_workers) as excutor:
                for category, terms in data.items():
                    for term, urls in terms.items():
                        for url in urls:
                            download_tasks.append(excutor.submit(self.download_image, url, category, term, pbar))
                            time.sleep(self.delay) # Polite delay
                            
                for future in as_completed(download_tasks):
                    print(future.result())
        
        self.export_filename()
        
    def export_filename(self):
        with open('filename.txt', 'w') as file:
            for filename in sorted(self.filename):
                file.write(f"{filename}\n")
                    
if __name__ == "__main__":
    downloader = ImageDownloader(json_file='image_urls.json', download_dir='Dataset', max_workers=4, delay=1)
    downloader.download_images()
    downloader.export_filename()