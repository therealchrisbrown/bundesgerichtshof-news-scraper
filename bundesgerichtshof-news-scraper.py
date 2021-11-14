import requests
from urllib import request
from bs4 import BeautifulSoup
import pandas as pd
from requests.api import head

# URL information
url = 'https://www.bundesgerichtshof.de/DE/Presse/Pressemitteilungen/pressemitteilungen_node.html'
page = request.urlopen(url).read().decode('utf8')

# HTML into python format
soup = BeautifulSoup(page, 'lxml')

# find specific table from tag <table>
table1 = soup.find('table', {'class': 'textualData links'})

# get every title of columns with tag <th>
headers = []
for i in table1.find_all('th'):
    title = i.text.replace(" ","").replace("\n","")
    headers.append(title)

jura_df = pd.DataFrame(columns=headers)


for j in table1.find_all('tr')[1:]:
    row_data = j.find_all('td')
    row = [i.text.replace(" ","").replace("\n","") for i in row_data]
    length = len(jura_df)
    jura_df.loc[length] = row

jura_df_link = []


for l in table1.find_all('tr')[1:]:
    link_data = l.find('a').get('href')
    jura_df_link.append('https://www.bundesgerichtshof.de/' + link_data)

jura_df['Link'] = jura_df_link

jura_df.to_csv('./jura_fin.csv',index=False)
