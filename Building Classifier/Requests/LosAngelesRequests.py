import pandas
import requests
import concurrent.futures
import math
parcelDir = "###/LosAngelesData.csv"
columns = [16, 85, 86] # Check these
imageDir = "###/Images/"
location = "LosAngeles"
requestLink = "https://cache.gis.lacounty.gov/cache/rest/services/LACounty_Cache/LACounty_Aerial_2014/MapServer/export?bbox="
data = pandas.read_csv(parcelDir, usecols=columns, header=0)
rowValue = 0
numRows = len(data.index)
p = 180/(math.pi)
c = 4.494382e-4

useDict = {
  **dict.fromkeys(["1700", "1710", "1720"], "Commercial/"), 
  **dict.fromkeys(["0100", "0101", "0104", "010D"], "Residential (Detached Houses)/"), 
  **dict.fromkeys(["010C", "010E"], "Residential (Attached Houses)/"), 
  **dict.fromkeys(["0300", "0301", "030A", "030B", "0350", "0351", "035A", "035B", "0400", "0401", "040A", "040B", "0450", "0451", "045A", "045B"], "Residential (Low Apartments)/"), 
  **dict.fromkeys(["0500", "0501", "0550", "0551"], "Residential (High Apartments)/"),
  **dict.fromkeys(["1800", "1810", "1820", "1830", "1840", "1850"], "Residential (Lodging)/"), 
  **dict.fromkeys(["3000", "3010", "3100", "3200", "3300", "3310", "3320", "3330", "3340", "3350", "3400", "3410", "3420", "3500", "3510", "3520", "3600", "3700", "3710", "3720", "3800", "3900", "3910", "3920", "8200", "8300"], "Industrial/"), 
  **dict.fromkeys(["7100", "7110", "7200", "7300", "8800", "8820", "8821", "8842", "8826", "8827", "8828", "8829", "8830", "8831", "8832", "8833", "8834", "8835", "8840"], "Institutional/"), 
  **dict.fromkeys(["1420", "2100", "2110", "2120", "2200", "2300", "2400", "2500", "2510", "2520", "2600", "2610", "2620", "2630", "2640", "2650", "2660", "2670", "6000", "6100", "6110", "6120", "6300", "6400", "6500", "6510", "6520", "6530", "6540", "1300", "1310", "1320", "1330", "1340", "1400", "1410", "1500", "1600"], "Retail/")
}

def getRequest(session, rowValue):
  lat = data.iloc[rowValue, 1]
  long = data.iloc[rowValue, 2]
  useCode = str(data.iloc[rowValue, 0])
  link = requestLink + str(long-c*math.cos(lat*p)) + "%2C" + str(lat-c) + "%2C" + str(long+c*math.cos(lat*p)) + "%2C" + str(lat+c) + "&bboxSR=4326&imageSR=4326&format=jpg&adjustAspectRatio=true&f=image"
  req = session.get(link, allow_redirects=True) # minlong, minlat, maxlong, maxlat
  name = imageDir + useDict.get(useCode, "Junk/") + str(rowValue) + "_" + location + ".jpg"
  with open(name, 'wb') as file:
    file.write(req.content)

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
  with requests.Session() as session:
    executor.map(getRequest, [session]*numRows, list(range(rowValue, numRows)))
    executor.shutdown(wait=True)
