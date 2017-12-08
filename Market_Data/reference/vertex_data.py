#### download vertex data
#$$
import datetime
import sys

todays_date = datetime.datetime.now()

year = todays_date.year
month = todays_date.month
day = todays_date.day
url_list = list()
products = list()

products.append('ZNZ7')
products.append('ZBZ7')
products.append('ZFZ7')
#products = ["ZNU7","ZBU7","ZFU7"]

for prod in products:
    url_list.append('http://restv3.vertex-analytics.com:8080/ECHO.eco/serv=FAST/user=uMirza/vers=201/form=3/type=7/symb='+ prod +'/helm_date=' 
+ todays_date.strftime("%Y%m%d") + '/helm_query=HELM_OREC_ALL')

#%% url import 
import urllib.request
import time

# local file path
file_path = 'C:\\Users (new)\\usman.mirza\\Documents\\Market Data\\'
logf = open("C:\\Users (new)\\usman.mirza\\Documents\\Market Data\\error_file.txt", "a")

# url list of rest API calls
for url in url_list:
    time.sleep(5)
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
            time.sleep(5)
            print(html)
        count = 0

# check if file is ready to download else set up 10 second timer to wait for 
        while 'READY' not in str(html) and count < 6:
            time.sleep(5)
            with urllib.request.urlopen(url) as response:
                html = response.read()
                count += 1
                time.sleep(5)
                print(html)
# when ready download product tick data
        if 'READY' in str(html):
            start = str(html).find('http://')
            end = str(html).find('.zip')
            download_url = str(html)[start:(end+4)]
        #find product symbol
            product_name = str(html)[(str(html).find('fLeadSymb')+14):(str(html).find('fLeadSymb')+18)]
            time.sleep(5)
            urllib.request.urlretrieve(download_url, file_path + product_name + '_' + todays_date.strftime("%Y%m%d") + '.zip')
            time.sleep(5)

    except Exception as e:
        logf.write("Failed to download {0}: {1}\n".format(str(url), str(e)))




