# -*- coding: utf-8 -*-
import requests

# last_price
lp_btc_jpy  = requests.get('https://api.zaif.jp/api/1/last_price/btc_jpy' )
lp_xem_jpy  = requests.get('https://api.zaif.jp/api/1/last_price/xem_jpy' )
lp_mona_jpy = requests.get('https://api.zaif.jp/api/1/last_price/mona_jpy')
lp_mona_btc = requests.get('https://api.zaif.jp/api/1/last_price/mona_btc')

# ticker
tc_btc_jpy  = requests.get('https://api.zaif.jp/api/1/ticker/btc_jpy' )
tc_xem_jpy  = requests.get('https://api.zaif.jp/api/1/ticker/xem_jpy' )
tc_mona_jpy = requests.get('https://api.zaif.jp/api/1/ticker/mona_jpy')
tc_mona_btc = requests.get('https://api.zaif.jp/api/1/ticker/mona_btc')

# trades
tr_btc_jpy  = requests.get('https://api.zaif.jp/api/1/trades/btc_jpy' )
tr_xem_jpy  = requests.get('https://api.zaif.jp/api/1/trades/xem_jpy' )
tr_mona_jpy = requests.get('https://api.zaif.jp/api/1/trades/mona_jpy')
tr_mona_btc = requests.get('https://api.zaif.jp/api/1/trades/mona_btc')

# depth
dp_btc_jpy  = requests.get('https://api.zaif.jp/api/1/depth/btc_jpy' )
dp_xem_jpy  = requests.get('https://api.zaif.jp/api/1/depth/xem_jpy' )
dp_mona_jpy = requests.get('https://api.zaif.jp/api/1/depth/mona_jpy')
dp_mona_btc = requests.get('https://api.zaif.jp/api/1/depth/mona_btc')

# currency_pairs
cp_all      = requests.get('https://api.zaif.jp/api/1/currency_pairs/all'    )
cp_btc_jpy  = requests.get('https://api.zaif.jp/api/1/currency_pairs/btc_jpy')

# currencies
cr_all      = requests.get('https://api.zaif.jp/api/1/currencies/all')
cr_btc      = requests.get('https://api.zaif.jp/api/1/currencies/btc')



# print
print(lp_btc_jpy.text)
print(tc_btc_jpy.text)
print(tr_btc_jpy.text)
print(dp_btc_jpy.text)
print(cp_btc_jpy.text)
print(cr_btc.text)

