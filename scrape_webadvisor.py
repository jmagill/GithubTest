import requests
from bs4 import BeautifulSoup
from itertools import chain

baseurl = 'https://webadvisor.iwcc.edu/WebAdvisor/WebAdvisor'
main_page = {'type': 'M', 'pid': 'CORE-WBMAIN'}
section_search = {'CONSTITUENCY': 'WBAP', 'type': 'P', 'pid': 'ST-WESTS12A'}

s = requests.Session()
s.params = {'TOKENIDX': ''}
r = s.get(baseurl, params=main_page)
s.params['TOKENIDX'] = r.cookies['LASTTOKEN']
r = s.get(baseurl, params=main_page)

r = s.get(baseurl, params=section_search)
r2 = s.post(r.request.url, data={
'VAR1': '18/SP',
'VAR9': 'Magill',
'LIST.VAR1_CONTROLLER': 'LIST.VAR1',
'LIST.VAR1_MEMBERS': 'LIST.VAR1*LIST.VAR2*LIST.VAR3*LIST.VAR4',
'LIST.VAR1_MAX': '5',
# Change to pull by course prefix
# 'LIST.VAR1_1': 'CSP',
})

# assert 'Intro Programming' in r2.text

soup = BeautifulSoup(r2.text, "lxml")
rows = soup.select('table[summary="Sections"] tr')
labels = [th.get_text(strip=True) for th in rows[1].find_all('th')[1:]]
course_data = [[td.get_text(strip=True) for td in row.find_all('td')[1:]] for row in rows[2:]]
col_widths = [max(map(len, chain((label,), (course[col] for course in course_data)))) for col, label in enumerate(labels)]
fmt = '|'.join('{{:{}}}'.format(w) for w in col_widths).format

with open('output.txt', 'w') as output:
    print(fmt(*labels))
    print('-' * (sum(col_widths) + len(col_widths) - 1))
    for course in course_data:
        print(fmt(*course))
