## Fetch vertex data
import sys
import datetime

todays_date = datetime.datetime.now()

year = todays_date.year
month = todays_date.month
day = todays_date.day
date = todays_date.strftime("%Y%m%d")  # 20171129

url_list = []
products = ["ZNZ7"]
#products = ["ZNU7", "ZBU7", "ZFU7"]

for prod in products:	
	date = '20171204'  
	url = ('http://restv3.vertex-analytics.com:8080/ECHO.eco/serv=FAST/user=uMirza/vers=201/form=3/type=7/symb=%s/helm_date=%s/helm_query=HELM_OREC_ALL'%(prod, date))
	url_list.append(url)

## URL Package 
import time 
import urllib.request 
import json
from JSONObject import JSONObject

delay_in_sec = 3
repeat_status_check = 6

file_path = 'E:\\Repos\\Quant\\Market_Data\\'
logf = open("E:\\Repos\\Quant\\Market_Data\\error_file.txt", "a")

# url list of rest API calls
for url in url_list:
	time.sleep(delay_in_sec)
	try:
		with urllib.request.urlopen(url) as response:
			html = response.read()
            ## Output formatted JSON data ## 
			#parsed = json.loads(html)
			#print (json.dumps(parsed, indent=4, sort_keys=True)) 
			time.sleep(delay_in_sec)
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
				time.sleep(delay_in_sec)
				#print(html)
			data = json.loads(html, object_hook=JSONObject)
			status = data.RTickLead.fExtnDesc

# when ready download product tick data
		if status.lower() == 'ready':
			download_url = data.RTickLead.fLeadPath
			#find product symbol
			product_name = data.RTickLead.fLeadSymb
			print(product_name)
			time.sleep(delay_in_sec)
			urllib.request.urlretrieve(download_url, file_path + product_name + '_' + todays_date.strftime("%Y%m%d") + '.zip')
			time.sleep(delay_in_sec)

	except Exception as e:
		logf.write("Failed to download {0}: {1}\n".format(str(url), str(e)))


'''
JSON data follow the following pattern below, 

{
    "RTickLead": {
        "fExtnDesc": "READY",
        "fLeadExtn": 0,
        "fLeadFile": "ZNZ7_20171204_10_OptRec_Events_20171204",
        "fLeadFlag": 0,
        "fLeadForm": 0,
        "fLeadMilt": 20171204,
        "fLeadPath": "http://Restv3.vertex-analytics.com:8080/V1/Data//ZNZ7_20171204/ZNZ7_20171204_10_OptRec_Events_20171204.zip",
        "fLeadProgL": 0,
        "fLeadProgT": 0,
        "fLeadStat": 0,
        "fLeadSymb": "ZNZ7",
        "fLeadVers": 0
    }
}
'''