import requests, json
from lxml import etree
import pandas as pd

def gather_results(rows):
  for row in rows:
    columns = row.cssselect("td.kompakt-lista__cell")
    if not columns: continue

    values = [
      columns[0].text,                      # Område
      columns[1].find('a').text,            # Adress
      columns[2].text,                      # Typ
      columns[3].text,                      # Våning
      (columns[4].xpath('text()')[1]
       .strip()) + 'm²',                    # Yta
      (columns[5].xpath('text()')[0]
       .replace(u'\xa0', u' ')).strip(),    # Hyra
      columns[6].xpath('text()')[0],         # Inflyttning
      columns[1].find('a').get('href'),
      ]

    yield dict(zip(headers, values))

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 13982.82.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.157 Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.gotlandshem.se/sok-ledigt/sok-ledigt-lista/?sortering=omrade&paginationantal=2147483647',
    'Accept-Language': 'sv',
}

params = {
    'sortering': 'omrade',
    'paginationantal': '2147483647',
    'callback': '',
    'widgets[]': [
        'objektlista@lagenheter',
    ],
}

response = requests.get('https://www.gotlandshem.se/widgets/', headers=headers, params=params)

d = json.loads(response.text.lstrip("(").rstrip(");"))['html']['objektlista@lagenheter']

table = etree.HTML(d).cssselect("table")[0]
rows = iter(table)

headers = [''.join(col.itertext()).strip() for col in next(rows).cssselect('th')] + ['Detaljsida']

results = [res for res in gather_results(rows)]

df = pd.DataFrame(results)
df.index += 1