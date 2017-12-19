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
DELAY_IN_SECOND = 2 # wait until the JSON data is fully loaded 


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


## Write symbols + instrumentID into a txt file 
import csv 

f = open('outfile.txt', 'w')
writer = csv.writer(f, delimiter=',')

for k, v in symbols.items():
	writer.writerow([k, v])