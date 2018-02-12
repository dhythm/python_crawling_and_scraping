from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from myproject.items import Headline

class NewsCrawlSpider(CrawlSpider):
    name = "news_crawl"
    # クロール対象とするドメインのリスト
    allowed_domains = ["news.yahoo.co.jp"]
    # クロールを開始する URL のリスト
    start_urls = (
        'http://news.yahoo.co.jp/',
    )

    # リンクをたどるためのルールのリスト
    rules = (
        # トピックスのページへのリンクを辿り、レスポンスを parse_topics() メソッドで処理する
        Rule(LinkExtractor(allow=r'/pickup/¥d+$'), callback='parse_topics'),
    )
    # 書籍ページとニュースページのリンクを辿り、それぞれ parse_book() と parse_news() メソッドで処理する
    rules = (
        Rule(LinkExtractor(allow=r'/book/¥w+'), callback='parse_book'),
        Rule(LinkExtractor(allow=r'/news/¥w+'), callback='parse_news'),
    )
    # カテゴリページ→商品ページへとリンクを辿り、 parse_product() メソッドで処理する
    rules = (
        Rule(LinkExtractor(allow=r'/category/¥w+')),
        Rule(LinkExtractor(allow=r'/product/¥w+'), callback='parse_product'),
    )
    # １つ前の例で、カテゴリページも parse_category() メソッドで処理する
    rules = (
        Rule(LinkExtractor(allow=r'/category/¥w+'), callback='parse_category', follow=True),
        Rule(LinkExtractor(allow=r'/product/¥w+'), callback='parse_product'),
    )

    def parse_topics(self, response):
        # トピックスのページからタイトルと本文を抜き出す
        item = Headline()
        item['title'] = response.css('.newsTitle ::text').extract_first()
        item['body'] = response.css('.hbody').xpath('string()').extract_first()
        yield item
