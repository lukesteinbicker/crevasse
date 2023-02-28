import pandas
import requests
import concurrent.futures
import math
parcelDir = "..." #path of parcel csv file
columns = [] #columns use in parcel csv
imageDir = "..." #directory where images are stored
location = "..." #location of images for documentation purposes
requestLink = "..." #first part of request
data = pandas.read_csv(parcelDir, usecols=columns, header=0)
rowValue = 0
numRows = len(data.index)
p = 180/(math.pi)
c = 4.494382e-4

useDict = { #use codes from parcel csv file are sorted into this use code dictionary
  **dict.fromkeys([], "Commercial/"), 
  **dict.fromkeys([], "Residential (Detached Houses)/"), 
  **dict.fromkeys([], "Residential (Attached Houses)/"), 
  **dict.fromkeys([], "Residential (Low Apartments)/"), 
  **dict.fromkeys([], "Residential (High Apartments)/"),
  **dict.fromkeys([], "Residential (Lodging)/"), 
  **dict.fromkeys([], "Industrial/"), 
  **dict.fromkeys([], "Institutional/"), 
  **dict.fromkeys([], "Retail/")
}

def getRequest(session, rowValue):
  lat = data.iloc[rowValue, 2]
  long = data.iloc[rowValue, 1]
  useCode = str(data.iloc[rowValue, 0])
  # Note: The coordinate system for each API varies. Most use WGS 84, but some use other spatial references. The line below converts a 100 x 100 meter box to degrees.
  link = requestLink + str(long-c*math.cos(lat*p)) + "%2C" + str(lat-c) + "%2C" + str(long+c*math.cos(lat*p)) + "%2C" + str(lat+c) + "..." #request parameters
  req = session.get(link, allow_redirects=True)
  name = imageDir + useDict.get(useCode, "Junk/") + str(rowValue) + "_" + location + ".jpg"
  with open(name, 'wb') as file:
    file.write(req.content)

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor: #parallelism to speed up requests
  with requests.Session() as session:
    executor.map(getRequest, [session]*numRows, list(range(rowValue, numRows)))
    executor.shutdown(wait=True)
