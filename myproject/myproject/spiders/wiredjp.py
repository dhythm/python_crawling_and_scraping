# -*- coding: utf-8 -*-
from scrapy.spiders import SitemapSpider


class WiredjpSpider(SitemapSpider):
    name = 'wiredjp'
    allowed_domains = ['wired.jp']
    # start_urls = ['http://wired.jp/']

    # サイトマップの URL リスト
    sitemap_urls = [
        'http://wired.jp/robots.txt',
    ]
    # サイトマップインデックスからたどる正規表現のリスト
    sitemap_follow = [
        r'post-2018-',
    ]
    # サイトマップに含まれる URL を処理するコールバック関数を指定するリスト
    sitemap_rules = [
        (r'/2018/\d\d/\d\d/', 'parse_post'),
    ]

    def parse_post(self, response):
        # 詳細ページから投稿のタイトルを抽出
        yield {
            'title': response.css('h1.post-title::text').extract_first(),
        }

