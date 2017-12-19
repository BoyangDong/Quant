## Get Instrument IDs

# URL Template: http://38.89.235.137:3011/V1/Instruments/CME/ZN?date=2017-08-07?uds=n

import datetime

todays_date = datetime.datetime.now()

year = todays_date.year
month = todays_date.month
day = todays_date.day
date = todays_date.strftime("%Y-%m-%d")  # 2017-12-18

file_path = 'E:\\Repos\\Quant\\Market_Data\\'
error_log = open("E:\\Repos\\Quant\\Market_Data\\option_fetcher_error.txt", "a")

url_list = []
types = ['ZN', 'ZB', 'ZF']
uds = ['n', 'y']  
date = '2017-08-07'
symbols = {} 

for t in types:
	for u in uds:
		url_list.append('http://38.89.235.137:3011/V1/Instruments/CME/%s?date=%s?uds=%s'%(t, date, u))	# 8 combinations 


import json 
import time 
import requests 
import urllib.request 
from JSONObject import JSONObject


NUM_OF_INSTRUMENTS = 3
DELAY_IN_SECOND = 3 # wait until the JSON data is fully loaded 


for url in url_list:
	print (url)
	try:
		with urllib.request.urlopen(url) as response:
			html = response.read()
			data = json.loads(html, object_hook=JSONObject)
			instruments = data.Instruments 
			time.sleep(DELAY_IN_SECOND)
			for i in range(NUM_OF_INSTRUMENTS):
				time.sleep(DELAY_IN_SECOND)
				instrumentId = instruments[i].instrumentId
				symbol = instruments[i].symbol
				symbols.update({symbol : instrumentId})
	
		#print(symbols)		
	
	except Exception as e:
		error_log.write("Failed to download {0}: {1}\n".format(str(url), str(e)))
'''
'''
## symbols{symbols : instrumentID} -> .csv
import csv 

file_name = 'outfile.txt'
f = open(file_name, 'w')
writer = csv.writer(f, delimiter=',')

for k, v in symbols.items():
	writer.writerow([k, v])	# symbols = products 


## .csv -> fetch options vertex data 

import sys
import time 
import urllib.request 
import json
from JSONObject import JSONObject


urls = []

#symbols = {'ZNU7': 357060, 'ZNZ7': 793429, 'ZNH8': 525443, 'ZBU7': 106225, 'ZBZ7': 439173, 'ZBH8': 333069, 'ZFU7': 134745, 'ZFZ7': 306580, 'ZFH8': 599339}
url_symbol_dict = {}

helm_date = todays_date.strftime("%Y%m%d")
helm_date = 20171129

for prod in symbols:	
	url = ('http://restv3.vertex-analytics.com:8080/ECHO.eco/serv=FAST/user=uMirza/vers=201/form=3/type=7/symb=%s/helm_date=%s/helm_query=HELM_OREC_ALL'%(prod, helm_date))
	urls.append(url)
	url_symbol_dict[url] = symbols[prod]


repeat_status_check = 6

logf = open("E:\\Repos\\Quant\\Market_Data\\error_file.txt", "a")

# url list of rest API calls
for url in urls:
	time.sleep(DELAY_IN_SECOND)
	try:
		with urllib.request.urlopen(url) as response:
			html = response.read()
			time.sleep(DELAY_IN_SECOND)
            #print(html)
		count = 0
		data = json.loads(html, object_hook=JSONObject)
		status = data.RTickLead.fExtnDesc 
		print(status)

# check if file is ready to download else set up 10 second timer to wait for 
		while status.lower() != 'ready' and count < repeat_status_check:
			with urllib.request.urlopen(url) as response:
				html = response.read()
				count += 1
				time.sleep(DELAY_IN_SECOND)
				#print(html)
			data = json.loads(html, object_hook=JSONObject)
			status = data.RTickLead.fExtnDesc

# when ready download product tick data
		if status.lower() == 'ready':
			download_url = data.RTickLead.fLeadPath
			#find product symbol
			product_name = data.RTickLead.fLeadSymb
			print(product_name)
			time.sleep(DELAY_IN_SECOND)
			urllib.request.urlretrieve(download_url, file_path + url_symbol_dict[url] + '_' + todays_date.strftime("%Y%m%d") + '.zip')
			time.sleep(DELAY_IN_SECOND)

	except Exception as e:
		logf.write("Failed to download {0}: {1}\n".format(str(url), str(e)))




