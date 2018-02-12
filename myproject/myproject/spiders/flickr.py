import os
from urllib.parse import urlencode

import scrapy


class FlickrSpider(scrapy.Spider):
    name = 'flickr'
    allowed_domains = ['api.flickr.com']

    def __init__(self, text='sushi'):
        super().__init__()

        self.start_urls = [
            'https://api.flickr.com/services/rest/?' + urlencode({
                'method': 'flickr.photos.search',
                'api_key': os.environ['FLICKR_API_KEY'],
                'text': text,
                'sort': 'relevance',
                'license': '4,5,9',
            }),
        ]

    def parse(self, response):
        for photo in response.css('photo'):
            yield {'file_urls': [flickr_photo_url(photo)]}

def flickr_photo_url(photo):
    return 'https://farm{farm}.staticflickr.com/{server}/{id}_{secret}_{size}.jpg'.format(
        farm=photo.xpath('@farm').extract_first(),
        server=photo.xpath('@server').extract_first(),
        id=photo.xpath('@id').extract_first(),
        secret=photo.xpath('@secret').extract_first(),
        size='b'
    )
