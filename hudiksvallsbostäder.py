import requests, lxml.html
from lxml import etree
import pandas as pd

data = {}
pages = []
url = 'https://www.hudiksvallsbostader.se/ledigt/lagenhet'

def gather_results(rows):
  for row in rows:
    columns = row.findall("td")
    if not columns: continue
    values = [
      columns[1].find('a').text,
      *[col.find('span').text.replace('\xa0', '.') for col in columns[2:]],
      ]
    yield dict(zip(headers, values))

s = requests.Session()
s.headers.update({
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'https://www.hudiksvallsbostader.se',
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 13982.82.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.157 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://www.hudiksvallsbostader.se/ledigt/lagenhet',
    'Accept-Language': 'sv,en;q=0.9,en-US;q=0.8',

})

response = s.get(url)

tree = lxml.html.fromstring(response.content)

table = etree.HTML(response.text).cssselect('table.gridlist')[0]
rows = iter(table)
headers = [''.join(col.itertext()).strip() for col in next(rows).cssselect('td.header')][1:]
results = [res for res in gather_results(rows)]

for d in tree.cssselect('.aspNetHidden > input'):
  data[d.name] = d.value

for p in tree.cssselect('div.navbar > div.text > span.right > a:not(.selected)'):
  pages.append(p.get('id').replace('_', '$'))

for page in pages:

  data.update({
    '__EVENTTARGET': page
  })
  
  response = requests.post(
    url,
    data=data
  )

  table = etree.HTML(response.text).cssselect('table.gridlist')[0]
  rows = iter(table)
  next(rows)

  results.extend([res for res in gather_results(rows)])

df = pd.DataFrame(results)
df.index += 1