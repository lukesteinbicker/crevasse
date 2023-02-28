import pandas
import requests
import concurrent.futures
import math
parcelDir = "###/NewYorkData.csv"
columns = [26, 73, 74] # Check these
imageDir = "###/Images/"
location = "NewYork"
requestLink = "https://orthos.its.ny.gov/arcgis/rest/services/wms/2022/MapServer/export?bbox="
data = pandas.read_csv(parcelDir, usecols=columns, header=0)
rowValue = 0
numRows = len(data.index)
p = 180/(math.pi)
c = 4.494382e-4

useDict = {
  **dict.fromkeys(["O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8", "O9"], "Commercial/"), 
  **dict.fromkeys(["A0", "A1", "A2", "A3", "A6"], "Residential (Detached Houses)/"), 
  **dict.fromkeys(["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "B1", "B2", "B3", "B9", "A4", "A5", "A7"], "Residential (Attached Houses)/"), 
  **dict.fromkeys(["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "CM"], "Residential (Low Apartments)/"), 
  **dict.fromkeys(["D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9"], "Residential (High Apartments)/"),
  **dict.fromkeys(["HB", "HH", "HR", "HS", "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9"], "Residential (Lodging)/"), 
  **dict.fromkeys(["E1", "E2", "E3", "E4", "E7", "E9", "F1", "F2", "F4", "F5", "F8", "F9"], "Industrial/"), 
  **dict.fromkeys(["I1", "M1", "M2", "M3", "M4", "M9", "P5", "P7", "P8", "W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9"], "Institutional/"), 
  **dict.fromkeys(["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9"], "Retail/")
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
