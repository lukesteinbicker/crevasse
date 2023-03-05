import pandas
import requests
import concurrent.futures
import math
parcelDir = "###/BuffaloData.csv"
columns = [8, 72, 73] # Check these
imageDir = "###/Images/"
location = "Buffalo"
requestLink = "https://gis.buffalony.gov/server/rest/services/Hosted/Buffalo2021/MapServer/export?bbox="
data = pandas.read_csv(parcelDir, usecols=columns, header=0)
rowValue = 0
numRows = len(data.index)
p = 180/(math.pi)
c = 4.494382e-4

useDict = {
  **dict.fromkeys(["460", "461", "462", "463", "464", "465"], "Commercial/"), 
  **dict.fromkeys(["210", "250"], "Residential (Detached Houses)/"), 
  **dict.fromkeys(["280", "281", "220", "230"], "Residential (Attached Houses)/"), 
  **dict.fromkeys(["411"], "Residential (Low Apartments)/"), 
  **dict.fromkeys([], "Residential (High Apartments)/"),
  **dict.fromkeys(["414", "415", "418"], "Residential (Lodging)/"), 
  **dict.fromkeys(["440", "441", "442", "443", "444", "445", "446", "447", "448", "449", "475", "710", "712", "714", "715", "720"], "Industrial/"), 
  **dict.fromkeys(["610", "611", "612", "613", "614", "615", "620", "630", "631", "632", "633", "640", "641", "642", "650"], "Institutional/"), 
  **dict.fromkeys(["420", "421", "422", "423", "424", "425", "426", "450", "451", "452", "453", "454", "455", "456", "457"], "Retail/")
}

def getRequest(session, rowValue):
  if rowValue % 1000 == 0:
    print(str(rowValue) + " rows complete")
  lat = data.iloc[rowValue, 2]
  long = data.iloc[rowValue, 1]
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
