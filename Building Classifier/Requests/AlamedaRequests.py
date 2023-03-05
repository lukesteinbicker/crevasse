import pandas
import requests
import concurrent.futures
parcelDir = "###/AlamedaData.csv"
columns = [12, 13, 40] # Check these
imageDir = "###/Images/"
location = "Alameda"
requestLink = "https://tiles.arcgis.com/tiles/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/Aerial_Imagery_2017/MapServer/export?bbox="
data = pandas.read_csv(parcelDir, usecols=columns, header=0)
rowValue = 0
numRows = len(data.index)
c = 164.042

useDict = {
  **dict.fromkeys(["9400", "9500"], "Commercial/"), 
  **dict.fromkeys(["1100"], "Residential (Detached Houses)/"), 
  **dict.fromkeys(["1500", "7300"], "Residential (Attached Houses)/"), 
  **dict.fromkeys(["7700"], "Residential (Low Apartments)/"), 
  **dict.fromkeys(["7800"], "Residential (High Apartments)/"),
  **dict.fromkeys(["8900", "9000"], "Residential (Lodging)/"), 
  **dict.fromkeys(["4000", "4100", "4102", "4103", "4200", "4201", "4202", "4205", "4300", "4400", "4600", "4601", "4700", "4800", "4900"], "Industrial/"), 
  **dict.fromkeys(["6100", "6400", "6600", "6700", "9910"], "Institutional/"), 
  **dict.fromkeys(["3100", "3400", "3500", "3600", "3605", "3610", "3700", "3701", "3702", "3703", "3704", "3705", "3800", "9200", "9300", "9600", "9700"], "Retail/")
}

def getRequest(session, rowValue):
  if rowValue % 1000 == 0:
    print(str(rowValue) + " rows complete")
  y = data.iloc[rowValue, 2]
  x = data.iloc[rowValue, 1]
  useCode = str(data.iloc[rowValue, 3])
  link = requestLink + str(x-c) + "%2C" + str(y-c) + "%2C" + str(x+c) + "%2C" + str(y+c) + "&bboxSR=102100&size=&imageSR=102100&format=jpg&adjustAspectRatio=true&f=image"
  req = session.get(link, allow_redirects=True) # minx, miny, maxx, maxy
  name = imageDir + useDict.get(useCode, "Junk/") + str(rowValue) + "_" + location + ".jpg"
  with open(name, 'wb') as file:
    file.write(req.content)

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
  with requests.Session() as session:
    executor.map(getRequest, [session]*numRows, list(range(rowValue, numRows)))
    executor.shutdown(wait=True)
