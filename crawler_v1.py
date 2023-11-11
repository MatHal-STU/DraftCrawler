import logging
from urllib.parse import urljoin
import re
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
        time.sleep(2)
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
            url=url,
            headers=headers
        )
        webpage = urlopen(req).read()
        return webpage

    def get_linked_urls(self, url, html):
        # draft_team = re.search('<strong>Draft<\/strong>: <a href="(\/)teams\/[^"]+\/draft.html">(.*?)<\/a>', soup).group(2).strip()
        # name = re.search('<h1> <span>(.*?)<\/span> <\/h1>', soup).group(1).strip()
        # draft_round = re.search('<strong>Draft<\/strong>: <a href="(\/)teams\/[^"]+\/draft.html">(.*?)<\/a>, (.*?) round \((.*?) overall\),', soup).group(3).strip()
        # draft_overall = re.search('<strong>Draft<\/strong>: <a href="(\/)teams\/[^"]+\/draft.html">(.*?)<\/a>, (.*?) round \((.*?) overall\),', soup).group(4).strip()
        # draft_year = re.search('<a href="\/draft\/NHL_(\d{4})_entry.html">(.*?)<\/a>', soup).group(1).strip() 
        # if re.search('<p><strong>Team Names:<\/strong>(.*?)<\/p>', html):
        soup = BeautifulSoup(html, 'html.parser')
        soup_ench = str(soup.encode("utf-8")).replace('\\n', ' ').replace('\\xc2\\xa0', ' ')

        with open(self.file_path, 'a', encoding="utf-8") as file:
            if re.search('<p><strong>Team Names:<\/strong>(.*?)<\/p>', soup_ench) or ( re.search('<h1> <span>(.*?)<\/span> <\/h1>', soup_ench) and re.search('<strong>Draft<\/strong>: <a href="(\/)teams\/[^"]+\/draft.html">(.*?)<\/a>', soup_ench) ):
                file.write(soup_ench)
        for link in soup.find_all('a'):
            path = link.get('href')
            if path is None:
                path = '/'
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url, html):
        if url not in self.visited_urls and url not in self.urls_to_visit and self.main_url in url:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url,html)

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
    Crawler('https://www.hockey-reference.com/', urls=['https://www.hockey-reference.com/draft/']).run()

# regex NHL_20(0[0-9]|1[0-9]|2[0-3]) a draft|player|team
# https://www.hockey-reference.com/draft/