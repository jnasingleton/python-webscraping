# This script pulls FSA/postal-codes from the Wikipedia directory of FSAs
# This script will include 'Not assigned' and 'Reserved' FSA Names
# This FSA to FSA details mapping is not freely avalable outside of Wikipedia, to the best of my knowledge.

import csv
import requests

from bs4 import BeautifulSoup

# Setup csv writer
csv_file = open('fsa_details.csv','wt',newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Province', 'Region', 'FSA Type', \
                     'FSA', 'FSA Name', 'FSA SubNames', \
                     'Postal Code', 'Postal Code Name', \
                     'FSA Usable'])

# Setup iterable parameters
fsa_letters = ['A', 'B', 'C', 'E', 'G', 'H', 'J', \
               'K', 'L', 'M', 'N', 'P', \
               'R', 'S', 'T', 'V', 'X', 'Y']
fsa_provinces = ['NL', 'NS', 'PE', 'NB', 'QC', 'QC', 'QC', \
               'ON', 'ON', 'ON', 'ON', 'ON', \
               'MB', 'SK', 'AB', 'BC', 'NU/NT', 'YT']

# Iterate webpages
for (letter, province) in zip(fsa_letters, fsa_provinces):

    url = 'https://en.wikipedia.org/wiki/List_of_' + letter + '_postal_codes_of_Canada'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    print(str(url))

    # Get region name
    region_name = soup.find_all('span', class_='mw-headline')[0]
    region_name = ''.join(region_name.find_all(text=True))
    region_name = region_name.rsplit(' ', 3)[0]
	
    # Seach tables for data
    tbl_index = 0
    for tbl in soup.find_all('table', rules='all'):
	
        # Determine tbl_type
        tbl_index += 1
        if tbl_index == 1:
            tbl_type = 'Urban';
        elif tbl_index == 2:
            tbl_type = 'Rural';
			
        # Iterate table cells
        for tr in tbl.find_all('tr'):
            for td in tr.find_all('td'):  
			
                # Get only text components
                td = ''.join(td.find_all(text=True))
				
                # Split by newlines and other whitespace
                td = [s.strip() for s in td.splitlines()]
				
                # Remove any blank array entries
                td = [s for s in td if len(s) > 0]
				
                # Extract data
                fsa = td[0];
                print(fsa)
                fsa_name = td[1];
				
                # Determine if fsa is useable
                if fsa_name == 'Not assigned' or fsa_name == 'Reserved' :
                    fsa_useable = False
                else:
                    fsa_useable = True   
					
                # Write to csv - Urban	
                if tbl_type == 'Urban':
                    try:
                        fsa_subnames = td[2];
                    except:
                        fsa_subnames = ''
                    postal_code = ''
                    postal_code_name = ''
                    csv_writer.writerow([province, region_name, tbl_type, \
                                         fsa, fsa_name, fsa_subnames, \
                                         postal_code, postal_code_name, \
                                         fsa_useable])
										 
                # Write to csv - Rural
                elif tbl_type == 'Rural':
                    fsa_subnames = ''
                    for bsa in td[2:]:
                        bsa = bsa.split(': ')
                        if len(bsa) == 2:
                            #-Create New Record
                            postal_code = fsa + bsa[0]
                            postal_code_name = bsa[1]
                            #If doesn't have a ":" split, 
                            #Append onto existing above postal code
                            csv_writer.writerow([province, region_name, tbl_type, \
                                                 fsa, fsa_name, fsa_subnames, \
                                                 postal_code, postal_code_name, \
                                                 fsa_useable])
                        else:
                            #-Update Previous Record
                            postal_code_name = bsa[0]
                            
# Close csv writer
csv_file.close()