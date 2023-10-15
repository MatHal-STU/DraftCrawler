import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, main_url, urls=[]):
        self.file_path = "html.txt"
        self.main_url = urls[0]
        self.visited_urls = []
        self.urls_to_visit = urls

    def download_url(self, url):
        req = Request(
            url= url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        )
        webpage = urlopen(req).read()
        return webpage

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        with open(self.file_path, 'a') as file:
            file.write(soup)
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