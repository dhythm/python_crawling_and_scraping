# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Headline(scrapy.Item):
    # ニュースのヘッドラインを表す Item

    title = scrapy.Field()
    body  = scrapy.Field()

class Restaurant(scrapy.Item):
    # 食べログのレストラン情報

    name = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    station = scrapy.Field()
    score = scrapy.Field()

class Page(scrapy.Item):
    # Web Page
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

    def __repr__(self):
        # ログへの出力時に長くなりすぎないように省略
        p = Page(self)
        if len(p['content']) > 100:
            p['content'] = p['content'][:100] + '...'

        return super(Page, p).__repr__()

# item = Headline()
# item['title'] = 'Example'
# print(item['title'])
