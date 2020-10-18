from datetime import datetime
import xml.etree.ElementTree as ET
import numpy as np
import requests

class FeedReader():
    def __init__(self, rss_file):
        self.rss_file = rss_file
        self.get_data()

    def get_data(self):
        urls = []
        self.data = []
        with open(self.rss_file) as f:
            for l in f.readlines():
                urls.append(l)
        for url in urls:
            self.parse(url)

    def parse(self, url):
        page = requests.get(url.strip())
        root = ET.fromstring(page.content)
        
        for item in root[0].findall('item'):
            entry = {}
            entry['title'] = item.find('title').text
            entry['description'] = item.find('description').text
            entry['link'] = item.find('link').text
            entry['pubDate'] = item.find('pubDate').text
            self.data.append(entry)
        
        self.data = self.sort_by_date()
    
    def sort_by_date(self):
        return sorted(self.data, key=lambda x: datetime.strptime(x.get('pubDate', 0), "%a, %d %b %Y %H:%M:%S %z").timestamp(), reverse=True)

if __name__=='__main__':
    fr = FeedReader('./resources/rss_feeds.txt')
    print(fr.data[0]['pubDate'])
    print(fr.data[-1]['pubDate'])

