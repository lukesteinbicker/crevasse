import pandas
import requests
import concurrent.futures
parcelDir = "###" # NEEDS TO BE CHANGED EVERY TIME
columns = [] # NEEDS TO BE CHANGED EVERY TIME
imageDir = "###" # NEEDS TO BE CHANGED EVERY TIME
location = "###" # NEEDS TO BE CHANGED EVERY TIME
requestLink = "###/exportImage?bbox=" # NEEDS TO BE CHANGED EVERY TIME
data = pandas.read_csv(parcelDir, usecols=columns, header=0)
rowValue = 0
numRows = len(data.index)

useDict = {
  **dict.fromkeys([], "Condos/"), # NEEDS TO BE CHANGED EVERY TIME
  **dict.fromkeys([], "DetachedHouses/"), # NEEDS TO BE CHANGED EVERY TIME
  **dict.fromkeys([], "RowHouses/"), # NEEDS TO BE CHANGED EVERY TIME
  **dict.fromkeys([], "Apartments/"), # NEEDS TO BE CHANGED EVERY TIME 
  **dict.fromkeys([], "Lodging/"), # NEEDS TO BE CHANGED EVERY TIME
  **dict.fromkeys([], "Industrial/"), # NEEDS TO BE CHANGED EVERY TIME 
  **dict.fromkeys([], "PublicBuildings/"), # NEEDS TO BE CHANGED EVERY TIME
  **dict.fromkeys([], "LargeCommercial/"), # NEEDS TO BE CHANGED EVERY TIME 
  **dict.fromkeys([], "SmallCommercial/"), # NEEDS TO BE CHANGED EVERY TIME
}

def getRequest(session, rowValue):
  link = requestLink + str(data.iloc[rowValue, 1]-0.0005) + "%2C" + str(data.iloc[rowValue, 2]-0.0005) + "%2C" + str(data.iloc[rowValue, 1]+0.0005) + "%2C" + str(data.iloc[rowValue, 2]+0.0005) + "&bboxSR=4326&size=&imageSR=4326&time=&format=jpg&pixelType=U8&noData=&noDataInterpretation=esriNoDataMatchAny&interpolation=+RSP_BilinearInterpolation&compression=&compressionQuality=&bandIds=&sliceId=&mosaicRule=&renderingRule=&adjustAspectRatio=true&validateExtent=false&lercVersion=1&compressionTolerance=&f=image"
  req = session.get(link, allow_redirects=True) # minlong, minlat, maxlong, maxlat
  name = imageDir + useDict.get(int(data.iloc[rowValue, 0]), "Junk/") + str(rowValue) + "_" + location + ".jpg"
  with open(name, 'wb') as file:
    file.write(req.content)

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
  with requests.Session() as session:
    executor.map(getRequest, [session]*numRows, list(range(rowValue, numRows)))
    executor.shutdown(wait=True)
