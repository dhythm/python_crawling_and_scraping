import logging

import lxml.html
import readability

logging.getLogger('readability.response').setLevel(logging.WARNING)

def get_content(html):
    # HTML の文字列から(タイトル，本文)のタプルを取得する
    document = readability.Document(html)
    content_html = document.summary()

    # HTML Tag を除去して本文のテキストのみを取得する
    content_text = lxml.html.fromstring(content_html).text_content().strip()
    short_title = document.short_title()
    return short_title, content_text
