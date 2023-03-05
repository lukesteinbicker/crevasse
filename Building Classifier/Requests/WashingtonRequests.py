import pandas
import requests
import concurrent.futures
import math
parcelDir = "###/WashingtonData.csv"
columns = [1, 2, 3] # Check these
imageDir = "###/Images/"
location = "Washington"
requestLink = "https://imagery.dcgis.dc.gov/dcgis/rest/services/Ortho/Ortho_2021/ImageServer/exportImage?bbox="
data = pandas.read_csv(parcelDir, usecols=columns, header=0)
rowValue = 0
numRows = len(data.index)
p = 180/(math.pi)
c = 4.494382e-4

useDict = {
  **dict.fromkeys(["50", "51", "52", "53", "54", "55", "56", "57", "58", "59"], "Commercial/"), 
  **dict.fromkeys(["12"], "Residential (Detached Houses)/"), 
  **dict.fromkeys(["11", "13", "16", "17"], "Residential (Attached Houses)/"), 
  **dict.fromkeys(["21"], "Residential (Low Apartments)/"), 
  **dict.fromkeys(["22"], "Residential (High Apartments)/"),
  **dict.fromkeys(["31", "32", "33", "35", "36", "37"], "Residential (Lodging)/"), 
  **dict.fromkeys(["71", "72", "73", "74", "75", "76", "77"], "Industrial/"), 
  **dict.fromkeys(["81", "83", "84", "85", "86"], "Institutional/"), 
  **dict.fromkeys(["41", "42", "43", "44", "45", "46", "47", "48", "49"], "Retail/")
}

def getRequest(session, rowValue):
  if rowValue % 1000 == 0:
   print(str(rowValue) + " rows complete")
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
