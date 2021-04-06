import requests
from bs4 import BeautifulSoup
from datetime import date
import time
import os 
import config

funds_track = ['ARKK', 'ARKQ', 'ARKW', 'ARKG', 'fintech-etf','3d-printing-etf','israel-etf']
today = date.today()

for fund in funds_track:
    url = "https://ark-funds.com/" + fund
    time.sleep(2.4)
    r = requests.get(url)
    if r: 
        soup = BeautifulSoup(r.content, 'lxml')
        table = None

        if fund not in ['3d-printing-etf','israel-etf']:
            table = soup.find('table', {"class":"avia-table-2"})
        else:
            print("Special URL funds")
            table = soup.find('table', {"class":"avia-table-3"})

        for row in table.find('tbody').find_all('tr'):
            for a in row.find_all('a', href=True):
                if a['href'][-3:] == 'csv':
                    fund_csv_url = a['href']
                    print ("Found the URL:", a['href'])
                    d3 = today.strftime("%Y-%m-%d")
                    print(d3)
                    req = requests.get(fund_csv_url)
                    url_content = req.content

                    try:  
                        if  not os.path.exists(config.DIR_DATA + '/' + d3): 
                            os.mkdir(config.DIR_DATA + '/' + d3)
                        
                        if fund == 'fintech-etf':
                            fund = 'ARKF'
                        elif fund == '3d-printing-etf':
                            fund = 'PRNT'
                        elif fund == 'israel-etf':
                            fund = 'IZRL'

                        csv_file = open(config.DIR_DATA + '/' + d3 + "/"+ fund +'.csv', 'wb')
                        csv_file.write(url_content)
                        csv_file.close()  
                    except OSError as error:  
                        print(error)   
    else:
        print(f'*Issues with URL of {fund}*')

