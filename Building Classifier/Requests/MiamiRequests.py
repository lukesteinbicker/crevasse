import pandas
import requests
import concurrent.futures
parcelDir = "###/MiamiData.csv"
columns = [2, 9, 10] # Check these
imageDir = "###/Images/"
location = "Miami"
requestLink = "https://imageserverintra.miamidade.gov/arcgis/rest/services/WGS1984_WebMercator/2021_Woolpert_WGS1984_WebMercator/ImageServer/exportImage?bbox="
data = pandas.read_csv(parcelDir, usecols=columns, header=0)
rowValue = 0
numRows = len(data.index)
c = 164.042

useDict = {
  **dict.fromkeys(["113", "170"], "Commercial/"), 
  **dict.fromkeys(["10", "11", "13"], "Residential (Detached Houses)/"), 
  **dict.fromkeys(["12"], "Residential (Attached Houses)/"), 
  **dict.fromkeys(["30"], "Residential (Low Apartments)/"), 
  **dict.fromkeys(["35", "180"], "Residential (High Apartments)/"),
  **dict.fromkeys(["200"], "Residential (Lodging)/"), 
  **dict.fromkeys(["300", "310", "320", "339", "342", "345", "370", "613", "620", "630", "631", "632"], "Industrial/"), 
  **dict.fromkeys(["400", "411", "412", "414", "420", "430", "440", "450", "451", "460", "470"], "Institutional/"), 
  **dict.fromkeys(["101", "110", "112"], "Retail/")
}

def getRequest(session, rowValue):
  y = data.iloc[rowValue, 2]
  x = data.iloc[rowValue, 1]
  useCode = str(data.iloc[rowValue, 0])
  link = requestLink + str(x-c) + "%2C" + str(y-c) + "%2C" + str(x+c) + "%2C" + str(y+c) + "&bboxSR=2881&imageSR=2881&format=jpg&adjustAspectRatio=true&f=image"
  req = session.get(link, allow_redirects=True) # minx, miny, maxx, maxy
  name = imageDir + useDict.get(useCode, "Junk/") + str(rowValue) + "_" + location + ".jpg"
  with open(name, 'wb') as file:
    file.write(req.content)

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
  with requests.Session() as session:
    executor.map(getRequest, [session]*numRows, list(range(rowValue, numRows)))
    executor.shutdown(wait=True)
