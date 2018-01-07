import sys
from selenium import webdriver

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

if __name__ == '__main__':
    main()
