import pandas
import numpy
import requests
import threading
import time
csvDir = "/home/mlnas/Desktop/Project/Backend/FILE.csv" #NEEDS TO BE CHANGED EVERY TIME
columns = [] #NEEDS TO BE CHANGED EVERY TIME
imageDir = "/home/mlnas/Desktop/Project/Images/ImagesSorted/"
location = "Place" #NEEDS TO BE CHANGED EVERY TIME
requestLink = "exportImage?bbox=" #NEEDS TO BE CHANGED EVERY TIME
data = pandas.read_csv(csvDir, usecols=columns, header=0)
numrows = len(data.index)
rowvalue = 0

usedict = dict.fromkeys( #NEEDS TO BE CHANGED EVERY TIME
    {"Condos/", "DetachedHouses/", "RowHouses/", "LargeApartmentBuildings/", "SmallApartmentBuildings/", "Lodging/", "Industrial/", "PublicBuildings/", "LargeBusiness/", "SmallBusiness/"},
	[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

coordmatrix = numpy.empty((4, numrows))

while rowvalue < numrows:
    coordmatrix[0, rowvalue] = data.iloc[rowvalue, 2] #long, NEEDS TO BE CHANGED EVERY TIME
    coordmatrix[1, rowvalue] = data.iloc[rowvalue, 1] #lat, NEEDS TO BE CHANGED EVERY TIME
    coordmatrix[2, rowvalue] = data.iloc[rowvalue, 0] #use code, NEEDS TO BE CHANGED EVERY TIME
    rowvalue += 1

def getRequest(link, imageDir, startValue):
	try:
		req = requests.get(link, allow_redirects=True)
		name = imageDir + usedict.get(coordmatrix[2, startValue], "Junk/") + str(startValue) + "_" + location + ".jpg"
		open(name, 'wb').write(req.content)
	except:
		print("Connection Failed, Retrying")
		time.sleep(10)

def getImagesThreaded(startValue, endValue):
        print("startValue, endValue:" + str(startValue) + "," + str(endValue))
        while startValue < endValue:
                link = requestLink + str(coordmatrix[0, startValue]-0.0005) + "%2C" + str(coordmatrix[1, startValue]-0.0005) + "%2C" + str(coordmatrix[0, startValue]+0.0005) + "%2C" + str(coordmatrix[1, startValue]+0.0005) + "&bboxSR=4326&size=&imageSR=4326&time=&format=jpg&pixelType=U8&noData=&noDataInterpretation=esriNoDataMatchAny&interpolation=+RSP_BilinearInterpolation&compression=&compressionQuality=&bandIds=&sliceId=&mosaicRule=&renderingRule=&adjustAspectRatio=true&validateExtent=false&lercVersion=1&compressionTolerance=&f=image"
                thread = threading.Thread(target=getRequest, args=(link, imageDir, startValue))
                thread.start()
                time.sleep(0.075)
                startValue += 1

rowvalue = 0

getImagesThreaded(rowvalue, numrows)
