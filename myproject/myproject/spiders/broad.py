# -*- coding: utf-8 -*-
import scrapy

from myproject.items import Page
from myproject.utils import get_content


class BroadSpider(scrapy.Spider):
    name = 'broad'
    start_urls = (
        'http://b.hatena.ne.jp/entrylist',
    )

    def parse(self, response):
        # 新着エントリーページをパースする

        # 個別のページリンクをたどる
        for url in response.css('a.entry-link::attr("href")').extract():
            yield scrapy.Request(url, callback=self.parse_page)

        url_more = response.css('a::attr("href")').re_first(r'.*\?of=\d{2}$')
        if url_more:
            # 絶対 URL に変換する
            yield scrapy.Request(response.urljoin(url_more))

    def parse_page(self, response):
        # 個別ページをパースする

        title, content = get_content(response.text)
        yield Page(url=response.url, title=title, content=content)
