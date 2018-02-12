import urllib
import datetime
import sqlite3
from bs4 import BeautifulSoup

# access
url = "http://www.nikkei.com/markets/kabu/"
html = urllib.request.urlopen(url)

# treat by BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

span = soup.find_all("span")
nikkei_avg = ""

for tag in span:
    try:
        string_ = tag.get("class").pop(0)

        if string_ in "mkc-stock_prices":
            nikkei_avg = tag.string
            break
    except:
        pass

conn = sqlite3.connect('nikkei-data.db')
c = conn.cursor()
# c.execute('DROP TABLE IF EXISTS nikkei')
c.execute('''
    CREATE TABLE IF NOT EXISTS nikkei (
        date text,
        average float
    )
''')
c.execute('INSERT INTO nikkei VALUES (?, ?)', (datetime.date.today(),nikkei_avg))
conn.commit()

c.execute('SELECT * FROM nikkei')
for row in c.fetchall():
    print(row)

conn.close()

# print(datetime.date.today(),',',nikkei_avg)
