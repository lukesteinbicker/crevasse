import pandas
import requests
import concurrent.futures
import math
parcelDir = "###/PhoenixData.csv"
columns = [6, 51, 52] # Check these
imageDir = "###/Images/"
location = "Phoenix"
requestLink = "https://gis.mcassessor.maricopa.gov/arcgis/rest/services/Aerials2022/MapServer/export?bbox="
data = pandas.read_csv(parcelDir, usecols=columns, header=0)
rowValue = 0
numRows = len(data.index)
p = 180/(math.pi)
c = 4.494382e-4

useDict = {
  **dict.fromkeys(["12", "15", "16"], "Commercial/"), 
  **dict.fromkeys(["01", "08"], "Residential (Detached Houses)/"), 
  **dict.fromkeys(["07"], "Residential (Attached Houses)/"), 
  **dict.fromkeys(["19"], "Residential (Low Apartments)/"), #subject to change
  **dict.fromkeys([], "Residential (High Apartments)/"),
  **dict.fromkeys(["04", "05", "06"], "Residential (Lodging)/"), 
  **dict.fromkeys(["30", "37"], "Industrial/"), 
  **dict.fromkeys(["97", "29"], "Institutional/"), 
  **dict.fromkeys(["10", "11", "13", "14", "17", "20", "25"], "Retail/")
}

useDict2 = {
  **dict.fromkeys(["0350", "0351", "0352", "0353", "0354", "0355", "0356", "0357", "0358"], "Residential (Low Apartments)/"),
  **dict.fromkeys(["0360", "0361", "0362", "0363", "0364", "0365", "0366", "0367", "0368", "0370", "0371", "0372", "0373", "0374", "0375", "0376", "0377", "0378"], "Residential (High Apartments)/"),
}

def getRequest(session, rowValue):
  if rowValue % 1000 == 0:
    print(str(rowValue) + " rows complete")
  lat = data.iloc[rowValue, 2]
  long = data.iloc[rowValue, 1]
  useCode = str(data.iloc[rowValue, 0])
  link = requestLink + str(long-c*math.cos(lat*p)) + "%2C" + str(lat-c) + "%2C" + str(long+c*math.cos(lat*p)) + "%2C" + str(lat+c) + "&bboxSR=4326&imageSR=4326&format=jpg&adjustAspectRatio=true&f=image"
  req = session.get(link, allow_redirects=True) # minlong, minlat, maxlong, maxlat
  if useCode[:2] == "03":
    name = imageDir + useDict2.get(useCode, "Junk/") + str(rowValue) + "_" + location + ".jpg"
    with open(name, 'wb') as file:
      file.write(req.content)
  else:
    name = imageDir + useDict.get(useCode[:2], "Junk/") + str(rowValue) + "_" + location + ".jpg"
    with open(name, 'wb') as file:
      file.write(req.content)

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
  with requests.Session() as session:
    executor.map(getRequest, [session]*numRows, list(range(rowValue, numRows)))
    executor.shutdown(wait=True)
