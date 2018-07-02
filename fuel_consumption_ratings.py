# This script downloads the csv files from the Canadain Fuel Consumption Ratings website.
# Additional work is required to process the headers of the csv file.
# A combine to csv function is applied after this script and further data analysis can occur using the consolidated csv file.

import pandas as pd
import urllib3

from bs4 import BeautifulSoup
from urllib import request

url = 'https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64'

http = urllib3.PoolManager()
response = http.request('GET', url, preload_content=False)

soup = BeautifulSoup(response.data, "html5lib")

for row in soup.find_all('tr'):
	row_cells = row.find_all('td')

	if len(row_cells) == 5:
		savefile = row_cells[0].text + '.csv'

		if 'Original' not in row_cells[0].text \
		and 'English' in row_cells[3].text:

			for link in row_cells[4].find_all('a', href=True):

				if 'Access' in link.text:
					url_csv = link['href']
					df = pd.read_csv(url_csv, header=None, encoding = 'latin1')
					# There are rows that are seperators that have column 5 NAN
					df.dropna(subset=[5], inplace=True)
					df.to_csv(savefile, encoding='utf-8', index=False)
					# To-Do: Fix headers
					# 1. Delete top rows and replace with manual header list
					# 2. Iterate between top 2 rows and combine to create a header list


