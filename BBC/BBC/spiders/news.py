import scrapy
from scrapy.spiders import Spider
import re


class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["bbc.com"]
    start_urls = ["https://www.bbc.com/news"]

    def start_requests(self):
        urls = [
            "https://www.bbc.com/news/live/world-europe-69007139?src_origin=BBCS_BBC/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Create a valid filename from the URL
        sanitized_url = re.sub(r"[^\w\-_\. ]", "_", response.url)
        filename = f"news-{sanitized_url}.html"
        with open(filename, "wb") as f:
            f.write(response.body)
        self.log(f"Saved file {filename}")
