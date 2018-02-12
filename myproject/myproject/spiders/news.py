# -*- coding: utf-8 -*-
import scrapy

from myproject.items import Headline


class NewsSpider(scrapy.Spider):
    # Spider の名前
    name = 'news'
    # クロール対象とするドメインのリスト
    allowed_domains = ['news.yahoo.co.jp']
    # クロールを開始する URL のリスト。
    start_urls = (
        'http://news.yahoo.co.jp/',
    )

    def parse(self, response):
        # トップページのトピックス一覧から個々のトピックスへのリンクを抜き出して表示する。
        for url in response.css('ul.topics a::attr("href")').re(r'/pickup/\d+$'):
            yield scrapy.Request(response.urljoin(url), self.parse_topics)

    def parse_topics(self, response):
        # トピックスのページからタイトルと本文を抜き出す。
        item = Headline()
        item['title'] = response.css('.newsTitle ::text').extract_first()
        item['body']  = response.css('.hbody').xpath('string()').extract_first()
        yield item
