
#!/usr/bin/env python3.5
# ------------------------- #
import requests
import bs4
from datetime import datetime

url = 'http://finance.yahoo.com/;_ylt=AwrTcdCNdhhXy7MAk3cnnIlQ;_ylu=X3oDMTByb2lvbXVuBGNvbG8DZ3ExBHBvcwMxBHZ0aWQDBHNlYwNzcg--'

def StockIndexer():
  response = requests.get(url)
  soup = bs4.BeautifulSoup(response.text, 'html.parser')

  # US Index
  SNP500 = soup.find(id="yfs_l84_^gspc").get_text()
  SNP500 = CleanUpReturn(SNP500)[0]
  Dow = soup.find(id="yfs_l84_^dji").get_text()
  Dow = CleanUpReturn(Dow)[0]
  Nasdaq = soup.find(id="yfs_l84_^ixic").get_text()
  Nasdaq = CleanUpReturn(Nasdaq)[0]

  # Asia Index
  Nikkei = soup.find(id="yfs_l84_^n225").get_text()
  Nikkei = CleanUpReturn(Nikkei)[0]
  HangSeng = soup.find(id="yfs_l84_^hsi").get_text()
  HangSeng = CleanUpReturn(HangSeng)[0]
  SSE = soup.find(id="yfs_l84_000001.ss").get_text()
  SSE = CleanUpReturn(SSE)[0]

  # Europe Index
  FTSE = soup.find(id="yfs_l84_^ftse").get_text()
  FTSE = CleanUpReturn(FTSE)[0]
  DAX = soup.find(id="yfs_l84_^gdaxi").get_text()
  DAX = CleanUpReturn(DAX)[0]
  CAC40 = soup.find(id="yfs_l84_^fchi").get_text()
  CAC40 = CleanUpReturn(CAC40)[0]

  print('--------------')
  print('US')
  print('--------------')
  print('{} | S&P 500  - ${}'.format(datetime.now(), SNP500))
  print('{} | Dow      - ${}'.format(datetime.now(), Dow))
  print('{} | Nasdaq   - ${}'.format(datetime.now(), Nasdaq))
  print()
  print('--------------')
  print('ASIA')
  print('--------------')
  print('{} | Nikkeo   - {}'.format(datetime.now(), Nikkei))
  print('{} | HangSeng - {}'.format(datetime.now(), HangSeng))
  print('{} | SSE      - {}'.format(datetime.now(), SSE))
  print()
  print('--------------')
  print('EUROPE')
  print('--------------')
  print('{} | FTSE     - {}'.format(datetime.now(), FTSE))
  print('{} | DAX      - {}'.format(datetime.now(), DAX))
  print('{} | CAC40    - {}'.format(datetime.now(), CAC40))
  print()
  print('All Done!')

def CleanUpReturn(item):
  item = item.strip()
  item = item.split( )
  return item
# ------------------------- #
if __name__ == '__main__':
  StockIndexer()
