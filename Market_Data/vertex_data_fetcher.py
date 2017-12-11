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

file_path = 'E:\\Repos\\Quant\\Market_Data\\'
logf = open("E:\\Repos\\Quant\\Market_Data\\error_file.txt", "a")

for url in url_list:
	try:
		with urllib.request.urlopen(url) as response:
			while True:			
				html = response.read()
				## Output formatted JSON data ## 
				#parsed = json.loads(html)
				#print (json.dumps(parsed, indent=4, sort_keys=True)) 
				data = json.loads(html, object_hook=JSONObject)
				status = data.RTickLead.fExtnDesc 
				print (status)
				if status.lower() == 'ready':
					download_url = data.RTickLead.fLeadPath
					print (download_url)
					product_name = data.RTickLead.fLeadSymb
				#	download_url = r'%s'% ('http://Restv3.vertex-analytics.com:8080/V1/Data//ZNZ7_20171204/ZNZ7_20171204_10_OptRec_Events_20171204.zip')
					urllib.request.urlretrieve(download_url, file_path + product_name + '_' + date + '.zip')
					time.sleep(10)
					break
			time.sleep(5)

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