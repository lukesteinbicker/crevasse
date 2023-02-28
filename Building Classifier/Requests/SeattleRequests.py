import pandas
import requests
import concurrent.futures
import math
parcelDir = "###/SeattleData.csv"
columns = [19, 20, 59] # Check these
imageDir = "###/Images/"
location = "Seattle"
requestLink = "https://gismaps.kingcounty.gov/arcgis/rest/services/BaseMaps/KingCo_Aerial_2021/MapServer/export?bbox="
data = pandas.read_csv(parcelDir, usecols=columns, header=0)
rowValue = 0
numRows = len(data.index)
p = 180/(math.pi)
c = 4.494382e-4

useDict = {
  **dict.fromkeys(["106", "118"], "Commercial/"), 
  **dict.fromkeys(["2", "3", "4", "5", "8"], "Residential (Detached Houses)/"), 
  **dict.fromkeys(["20", "25", "29"], "Residential (Attached Houses)/"), 
  **dict.fromkeys(["11", "17", "18"], "Residential (Low Apartments)/"), 
  **dict.fromkeys(["16"], "Residential (High Apartments)/"),
  **dict.fromkeys(["51", "55", "56", "57", "58", "59"], "Residential (Lodging)/"), 
  **dict.fromkeys(["138", "195", "202", "210", "216", "223", "245", "246", "247", "252", "261", "262", "263", "264"], "Industrial/"), 
  **dict.fromkeys(["165", "172", "173", "184", "185"], "Institutional/"), 
  **dict.fromkeys(["60", "61", "62", "63", "64", "96", "101", "104", "105", "122", "140", "162", "163", "166", "167", "171", "191", "194"], "Retail/")
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
