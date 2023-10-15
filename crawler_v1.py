import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
import random 

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, main_url, urls=[]):
        self.file_path = "html.txt"
        self.main_url = main_url
        self.visited_urls = []
        self.urls_to_visit = urls
        with open(self.file_path, 'w'):
            pass  
    def download_url(self, url):
        time.sleep(5)
        user_agents = [ 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
	        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
	        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
	        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
	        'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36' 
        ]
        user_agent = random.choice(user_agents) 
        headers = {'User-Agent': user_agent} 
        req = Request(
            url= url, 
            headers= headers
        )
        webpage = urlopen(req).read()
        return webpage

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        with open(self.file_path, 'a') as file:
            file.write(str(soup))
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit and self.main_url in url:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

if __name__ == '__main__':
    Crawler('https://www.hockeydb.com/', urls=['https://www.hockeydb.com/ihdb/draft/index.html']).run()