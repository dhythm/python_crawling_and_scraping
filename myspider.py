import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    # クロールを開始する URL のリスト
    start_urls = ['https://blog.scrapinghub.com']

    def parse(self, response):
        # トップページからカテゴリページへのリンクを抜き出してたどる
        for url in response.css('ul li a::attr("href")').re('.*/category/.*'):
            yield scrapy.Request(response.urljoin(url), self.parse_titles)

    def parse_titles(self, response):
        # カテゴリページからそのカテゴリの投稿のタイトルをすべて抜き出す
        for post_title in response.css('div.entries > ul > li a::text').extract():
            yield {'title': post_title}

    """
    def parse(self, response):
        for title in response.css('h2.entry-title'):
            yield {'title': title.css('a ::text').extract_first()}

        for next__page in response.css('div.prev-post > a'):
            yield response.follow(next__page, self.parse)
    """
