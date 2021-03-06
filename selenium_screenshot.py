import sys
import time

import json
import base64

from PIL import Image

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def main():

    f = open('access.json','r')
    json_dict = json.load(f)

    # プロキシ設定
    proxies = {
        'host': '',
        'port': '',
        'username': '',
        'password': ''
    }
    proxyauth_plugin_path = create_proxyauth_extension(
        proxy_host=proxies['host'],
        proxy_port=proxies['port'],
        proxy_username=proxies['username'],
        proxy_password=proxies['password']
    )

    # 野村證券のスクレイピング
    site = 'nomura-sec'
    branch_number = json_dict[site]['branch']
    account_number = json_dict[site]['account']
    password = base64.b64decode(json_dict[site]['password']).decode('utf-8')

    # WebDriver オブジェクトを生成
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # options.add_extension(proxyauth_plugin_path) # ヘッドレスモードでは拡張機能はサポート外
    driver = webdriver.Chrome(chrome_options=options)

    # タイムアウト設定
    driver.set_page_load_timeout(10)
    wait = WebDriverWait(driver, 10)

    # ログイン画面
    url = 'https://hometrade.nomura.co.jp'
    driver.get(url)
    # time.sleep(5)
    full = True
    notfull = False
    save_screenshot(driver, './001.png', full)

    # 認証情報を入力する
    driver.find_element_by_id('branchNo').send_keys(branch_number)
    driver.find_element_by_id('accountNo').send_keys(account_number)
    driver.find_element_by_id('passwd1').send_keys(password)
    driver.find_element_by_name('buttonLogin').send_keys(Keys.RETURN)
    # time.sleep(5)

    # トップページ
    save_screenshot(driver, './002.png', full)

    # サービス・契約情報紹介/変更
    # driver.find_element_by_partial_link_text('口座情報').send_keys(Keys.RETURN)
    driver.find_element_by_css_selector('a[href="#nav-contents07"]').send_keys(Keys.RETURN)
    save_screenshot(driver, './003.png', )
    # driver.find_element_by_partial_link_text('サービス・契約').send_keys(Keys.RETURN)
    driver.find_element_by_css_selector('a[href="rmfActCusRgiRefListAction.do"]').send_keys(Keys.RETURN)
    # time.sleep(2)
    save_screenshot(driver, './004.png', full)
    # ご投資状況
    # driver.find_element_by_partial_link_text('資産状況').send_keys(Keys.RETURN)
    driver.find_element_by_css_selector('a[href="#nav-contents02"]').send_keys(Keys.RETURN)
    save_screenshot(driver, './005.png', )
    # driver.find_element_by_partial_link_text('ご投資状況').send_keys(Keys.RETURN)
    driver.find_element_by_css_selector('a[href="rmfAstAdpInvLstAction.do"]').send_keys(Keys.RETURN)
    
    # time.sleep(2)
    save_screenshot(driver, './006.png', full)

    # print(driver.page_source)
    driver.close()

def create_proxyauth_extension(proxy_host, proxy_port,
                               proxy_username, proxy_password,
                               scheme='http', plugin_path=None):
    import string
    import zipfile

    if plugin_path is None:
        plugin_path = './chrome_proxyauth_plugin.zip'

    manifest_json = """
    {
      "version": "1.0.0",
      "manifest_version": 2,
      "name": "Chrome Proxy",
      "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
      ],
      "background": {
          "scripts": ["background.js"]
      },
      "minimum_chrome_version":"22.0.0"
    }
    """
    background_js = string.Template(
    """
    var config = {
      mode: "fixed_servers",
      rules: {
        singleProxy: {
          scheme: "${scheme}",
          host: "${host}",
          port: parseInt(${port})
        },
        bypassList: [
          "*localhost*"
        ]
      }
    };
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    function callbackFn(details) {
      return {
        authCredentials: {
          username: "${username}",
          password: "${password}"
        }
      };
    }
    chrome.webRequest.onAuthRequired.addListener(
      callbackFn,
      {urls: ["<all_urls>"]},
      ['blocking']
    );
    """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path

def save_screenshot(self, filename, fullsize=False):
    filepath = '/'.join(filename.split('/')[:-1])
    if fullsize:
        # ページの左上までスクロール
        self.execute_script("window.scrollTo(0,0);")

        # ページサイズの取得
        total_height = self.execute_script("return document.body.scrollHeight")
        total_width  = self.execute_script("return document.body.scrollWidth")

        # 画面サイズの取得
        view_height = self.execute_script("return window.innerHeight")
        view_width  = self.execute_script("return window.innerWidth")

        # 画像処理用
        stitched_image = Image.new("RGB", (total_width, total_height))

        # スクロール操作用
        scroll_width  = 0
        scroll_height = 0

        row_count = 0
        # 縦スクロールの処理
        while scroll_height < total_height:
            # 横スクロール初期化
            col_count = 0
            scroll_width = 0
            self.execute_script("window.scrollTo({0}, {1})".format(scroll_width, scroll_height))
            # 横スクロールの処理
            while scroll_width < total_width:
                if col_count > 0:
                    # 画面サイズ分のスクロール
                    self.execute_script("window.scrollBy(",str(view_width),",0)")

                tmpname = '{0}/tmp_{1}_{2}.png'.format(filepath, row_count, col_count)
                self.get_screenshot_as_file(tmpname)
                time.sleep(1)

                # 右端か、下端に到達したら画像を切り取って stitched_image に貼り付け
                sum_w = scroll_width + view_width
                sum_h = scroll_height + view_height
                if sum_w >= total_width or sum_h >= total_height:
                    new_width  = view_width
                    new_height = view_height
                    if sum_w >= total_width:
                        new_width = total_width - scroll_width
                    if sum_h >= total_height:
                        new_height = total_height - scroll_height
                    tmp_image = Image.open(tmpname)
                    tmp_image.crop((view_width - new_width, view_height - new_height, view_width, view_height)).save(tmpname)
                    stitched_image.paste(Image.open(tmpname), (scroll_width, scroll_height))
                    scroll_width += new_width
                # 通常の貼り付け
                else:
                    stitched_image.paste(Image.open(tmpname), (scroll_width, scroll_height))
                    scroll_width += view_width
                    col_count += 1

            scroll_height += view_height
            time.sleep(1)

        # 指定の filename に stitched_image を格納
        stitched_image.save(filename)
        return True

    # fullsize=False の場合は通常のスクリーンショットを取得
    else:
        self.get_screenshot_as_file(filename)

if __name__ == '__main__':
    start = time.time()
    main()
    elapsed_time = time.time() - start
    print("elapsed_time:{0:0.2f}".format(elapsed_time) + "[sec]")

