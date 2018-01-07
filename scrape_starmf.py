import sys
import os

from robobrowser import RoboBrowser

browser = RoboBrowser(
    parser='html.parser',
    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecho/20100101 Firefox/45.0'
)

def main():

    # コマンドライン引数からログイン項目をセット
    store_code = sys.argv[1]
    account_number = sys.argv[2]
    password = sys.argv[3]

    browser.open('https://hometrade.nomura.co.jp/web/rmfIndexWebAction.do')

    form = browser.get_form(action='/web/rmfCmnCauSysLgiAction.do')
    form['btnCd'] = store_code
    form['kuzNo'] = account_number
    form['gnziLoginPswd'] = password
    # print(form)
    browser.submit_form(form)

    action_name = browser.url.split('/')[-1]
    # print(browser.parsed)
    # print(browser.url)
    # print(action_name)

    # TODO  ログインに成功した後の処理
    # rmfCmnCauSysLgaEtdDocAgreemAction.do
    if action_name == 'rmfCmnCauSysLgaEtdDocAgreemAction.do':
        print('ログイン成功')
    # TODO  ログインに失敗した場合の処理
    # rmfCmnCauSysLgiAction.do
    else:
        print('ログイン失敗')

# スクリプトファイルを直接実行した場合のみ、動作する
if __name__ == '__main__':
    main()

