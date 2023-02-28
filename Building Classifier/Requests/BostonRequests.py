import pandas
import requests
import concurrent.futures
import math
parcelDir = "###/BostonData.csv"
columns = [8, 72, 73] # Check these
imageDir = "###/Images/"
location = "Boston"
requestLink = "https://tiles.arcgis.com/tiles/hGdibHYSPO59RG1h/arcgis/rest/services/orthos2021/MapServer/export?bbox="
data = pandas.read_csv(parcelDir, usecols=columns, header=0)
rowValue = 0
numRows = len(data.index)
p = 180/(math.pi)
c = 4.494382e-4

useDict = {
  **dict.fromkeys(["340", "343", "344", "345", "346", "347", "348", "965"], "Commercial/"), 
  **dict.fromkeys(["101", "103"], "Residential (Detached Houses)/"), 
  **dict.fromkeys(["102", "104", "105"], "Residential (Attached Houses)/"), 
  **dict.fromkeys(["111", "112"], "Residential (Low Apartments)/"), 
  **dict.fromkeys(["113", "114"], "Residential (High Apartments)/"),
  **dict.fromkeys(["300", "301", "302"], "Residential (Lodging)/"), 
  **dict.fromkeys(["313", "314", "315", "316", "317", "318", "400", "401", "402", "403", "404", "405", "406", "407", "408", "409", "410", "411", "412", "413", "414", "415", "416", "417", "440"], "Industrial/"), 
  **dict.fromkeys(["350", "351", "360", "970", "976", "977", "978"], "Institutional/"), 
  **dict.fromkeys(["319", "320", "321", "322", "323", "324", "325", "326", "327", "328", "329", "341", "342", "361", "362", "370"], "Retail/")
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
