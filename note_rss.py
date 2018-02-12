import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import feedgenerator

def main():
    driver = webdriver.PhantomJS()
    driver.set_window_size(800,600)

    navigate(driver)
    posts = scrape_posts(driver)

    # RSS フィードとして保存
    with open('recommend.rss','w') as f:
        save_as_feed(f,posts)

def navigate(driver):
    # 目的のページに遷移
    print('Navigating...', file=sys.stderr)
    # note のトップページを開く
    driver.get('https://note.mu/')
    assert 'note' in driver.title

def scrape_posts(driver):
    # 文章コンテンツの URL、タイトル、概要を含む dict のリストを取得
    posts = []

    # すべての文章コンテンツを表す a 要素について反復
    for a in driver.find_elements_by_css_selector('a.p-post--basic'):
        posts.append({
            'url'           : a.get_attribute('href'),
            'title'         : a.find_element_by_css_selector('h4').text,
            'description'   : a.find_element_by_css_selector('.c-post__description').text,
        })

    return posts

def save_as_feed(f,posts):
    # 文章コンテンツをリストをフィードとして保存
    # フィードを表す Rss201rev2Feed オブジェクトを作成
    feed = feedgenerator.Rss201rev2Feed(
        title='おすすめノート',
        link='https://note.mu/',
        description='おすすめノート')

    for post in posts:
        feed.add_item(title=post['title'], link=post['url'], description=post['description'], unique_id=poost['url'])

    feed.write(f, 'utf-8')

if __name__ == '__main__':
    main()
