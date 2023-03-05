import pandas
import requests
import concurrent.futures
import math
parcelDir = "###/ChicagoData.csv"
columns = [3, 12, 13] # Check these
imageDir = "###/Images/"
location = "Chicago"
requestLink = "https://gis.cookcountyil.gov/imagery/rest/services/CookOrtho2021/ImageServer/exportImage?bbox="
data = pandas.read_csv(parcelDir, usecols=columns, header=0)
rowValue = 0
numRows = len(data.index)
p = 180/(math.pi)
c = 4.494382e-4

useDict = {
  **dict.fromkeys(["791", "774"], "Commercial/"), 
  **dict.fromkeys(["200", "202", "203", "204", "205", "206", "207", "208", "209", "234", "278"], "Residential (Detached Houses)/"), 
  **dict.fromkeys(["210", "295", "396", "299", "399", "599"], "Residential (Attached Houses)/"), 
  **dict.fromkeys(["211", "212", "313", "314", "315"], "Residential (Low Apartments)/"), 
  **dict.fromkeys(["318", "391"], "Residential (High Apartments)/"),
  **dict.fromkeys(["529"], "Residential (Lodging)/"), 
  **dict.fromkeys(["593"], "Industrial/"), 
  **dict.fromkeys([], "Institutional/"), 
  **dict.fromkeys(["517", "528", "523", "527", "530", "531", "532"], "Retail/")
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
