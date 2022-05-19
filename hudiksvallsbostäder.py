import requests, lxml.html
import pandas as pd

data = {}
url = 'https://www.hudiksvallsbostader.se/ledigt/lagenhet'

def gather_results(rows):
  for row in rows:
    columns = row.findall("td")
    if not columns: continue

    values = [
      columns[1].find('span').text,
      columns[2].find('a').text,
      *[col.find('span').text.replace('\xa0', '.') for col in columns[3:]],
      url.replace('lagenhet', columns[2].find('a').get("href")),
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
table = tree.cssselect('table.gridlist')[0]

rows = iter(table)
headers = [''.join(col.itertext()).strip() for col in next(rows).cssselect('td.header')][1:] + ['Detaljsida']
results = [res for res in gather_results(rows)]

for d in tree.cssselect('.aspNetHidden > input'):
  data[d.name] = d.value

num_of_pages = int(tree.cssselect('#ctl00_ctl01_DefaultSiteContentPlaceHolder1_Col1_ucNavBar_lblNoOfPages')[0].text)

# we start at 2 because page 1 is already collected
for N in range(2, num_of_pages+1):
  data.update({
    '__EVENTTARGET': 'ctl00$ctl01$DefaultSiteContentPlaceHolder1$Col1$ucNavBar$btnNavNext'
  })

  response = s.post(
    url,
    data=data
  )

  tree = lxml.html.fromstring(response.content)
  table = tree.cssselect('table.gridlist')[0]
  rows = iter(table)
  next(rows)

  results.extend([res for res in gather_results(rows)])

  if N < num_of_pages:
    for d in tree.cssselect('.aspNetHidden > input'):
      data[d.name] = d.value

df = pd.DataFrame(results)
df.index += 1
