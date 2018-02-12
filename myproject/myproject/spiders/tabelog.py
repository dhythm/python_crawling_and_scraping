# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from myproject.items import Restaurant


class TabelogSpider(CrawlSpider):
    name = 'tabelog'
    allowed_domains = ['tabelog.com']
    start_urls = (
        'http://tabelog.com/tokyo/rstLst/lunch/?LstCosT=2&RdoCosTp=1',
    )

    rules = [
        Rule(LinkExtractor(allow=r'/\w+/rstLst/lunch/\d/')),
        Rule(LinkExtractor(allow=r'/\w+/A\d+/A\d+/\d+/$'), callback='parse_restaurant'),
    ]

    def parse_restaurant(self, response):
        latitude, longitude = response.css(
            'img.js-map-lazyload::attr("data-original")').re(
                r'markers=.*?%7C([\d.]+),([\d.]+)')
        item = Restaurant(
            name=response.css('.display-name').xpath('string()').extract_first().strip(),
            address=response.css('.rstinfo-table__address').xpath('string()').extract_first().strip(),
            
            latitude=latitude,
            longitude=longitude,
            station=response.css('dt:contains("最寄り駅")+dd span::text').extract_first(),
            score=response.css('#js-header-rating span::text').extract_first(),
        )
        yield item
