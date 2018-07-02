# This script extracts the geographies belonging to Canadian CMAs/CAs based on the 2016 census.
# This data is (surprisingly) not available for download in the census data files.

# Import Selenium Libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FOptions 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

import csv

# Set Selenium Options
options = FOptions()
options.set_headless(headless=True)
#options.set_headless(headless=False)
driver = webdriver.Firefox(firefox_options=options, executable_path=r'C:\Utility\BrowserDrivers\geckodriver.exe')

# Set Driver to Provided URL
url = 'http://www12.statcan.gc.ca/census-recensement/2016/dp-pd/hlt-fst/pd-pl/Table.cfm?Lang=Eng&T=303&SR=1&S=86&O=A&RPP=9999' 
driver.get(url)

# Setup csv writer
csv_filename = 'CMAs-CAs_municipalities.csv'
csv_file = open(csv_filename,'wt',newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['CMA-CA', 'Geographic_Name', 'Geographic_Type', \
                     'Population_2016', 'Population_2011', 'Population_%_Change', \
                     'Private_Dwellings_2016_Total', 'Private_Dwellings_2016_Occupied_By_Usual', 'Land_Use_(km2)_2016', \
                     'Population_Density_(/km2)_2016', 'CD/CSD_Population_Rank_2016_National', 'CD/CSD_Population_Rank_2016_Prov/Terr'])

# Set webdriver wait_time
wait_time = 30

# Set wait for the driver
driver_wait = WebDriverWait(driver, wait_time)

dropdown_element = driver_wait.until(EC.element_to_be_clickable((By.ID, 'CMA')))
dropdown_list = dropdown_element.text.split('\n')

for dropdown_index in range(len(dropdown_list)):

	print(dropdown_index,dropdown_list[dropdown_index])

	dropdown_element = driver_wait.until(EC.element_to_be_clickable((By.ID, 'CMA')))
	selected_dropdown_element = Select(dropdown_element)
	selected_dropdown_element.select_by_index(dropdown_index)

	submit_element = driver_wait.until(EC.element_to_be_clickable((By.ID, 'subgeo')))
	submit_element.click()

	tbody_elements = driver.find_elements_by_tag_name('tbody')
	#tbody_elements[0] is the blank header row
	tbody_element = tbody_elements[1]

	tr_elements = tbody_element.find_elements_by_tag_name('tr')
	for tr_element in tr_elements:

		list_values = []
		list_values.append(dropdown_list[dropdown_index])

		th_element = tr_element.find_element_by_tag_name('th')
		list_values.append(th_element.text)

		td_elements = tr_element.find_elements_by_tag_name('td')
		for td_element in td_elements:
			list_values.append(td_element.text)

		csv_writer.writerow(list_values)

# Close csv writer
csv_file.close()

