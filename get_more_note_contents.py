import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def main():
    # PhantomJS の WebDriver オブジェクトを生成
    driver = webdriver.PhantomJS()
    # ウィンドウサイズを設定
    driver.set_window_size(800,600)


    # note のトップページに遷移
    navigate(driver)
    # 文章コンテンツのリストを取得
    posts = scrape_posts(driver)

    for post in posts:
        print(post)


def navigate(driver):
    print('Navigating...', file=sys.stderr)
    driver.get('https://note.mu/')
    assert 'note' in driver.title

    # ページの一番下までスクロールする
    time.sleep(2)
    driver.execute_script('scroll(0, document.body.scrollHeight)')

    print('Waiting for contents to be loaded...', file=sys.stderr)
    time.sleep(2)
    driver.execute_script('scroll(0, document.body.scrollHeight)')

    time.sleep(2)
    driver.execute_script('scroll(0, document.body.scrollHeight)')

    # 10秒でタイムアウトする WebDriverWait オブジェクトを作成
    wait = WebDriverWait(driver, 10)

    print('Waiting for the more button to be clickable...', file=sys.stderr)
    # 「もっとみる」ボタンがクリック可能になるまで待つ
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-more')))
    button.click()

    print('Waiting for contents to be loaded...', file=sys.stderr)
    time.sleep(2)

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

if __name__ == '__main__':
    main()
