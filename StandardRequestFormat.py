import pandas
import numpy
import requests
import threading
import time
import multiprocessing
csvDir = "/home/mlnas/Desktop/Project/Backend/FILE.csv" # NEEDS TO BE CHANGED EVERY TIME
columns = []  # NEEDS TO BE CHANGED EVERY TIME
imageDir = "/home/mlnas/Desktop/Project/Images/ImagesSorted/"
location = "Place"  # NEEDS TO BE CHANGED EVERY TIME
requestLink = "exportImage?bbox="  # NEEDS TO BE CHANGED EVERY TIME
data = pandas.read_csv(csvDir, usecols=columns, header=0) # ONLY INCLUDE USE CODE, LAT, AND LONG

usedict = dict.fromkeys(  # NEEDS TO BE CHANGED EVERY TIME
    {"Condos/", "DetachedHouses/", "RowHouses/", "LargeApartmentBuildings/", "SmallApartmentBuildings/", "Lodging/", "Industrial/", "PublicBuildings/", "LargeBusiness/", "SmallBusiness/"},
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

coordmatrix = numpy.empty((4, len(data.index)))

def matrixCreation(i):
    index = 0
    while index < len(data.index):
        coordmatrix[i, index] = data.iloc[index, i]
        index += 1

def getRequest(link, imageDir, startValue):
    try:
        req = requests.get(link, allow_redirects=True)
        name = imageDir + usedict.get(coordmatrix[2, startValue], "Junk/") + str(startValue) + "_" + location + ".jpg"
        open(name, 'wb').write(req.content)
    except:
        n = 0
        while n < 1000000:
            n += 1

def getImagesThreaded(startValue, endValue):
    print("startValue, endValue:" + str(startValue) + "," + str(endValue))
    while startValue < endValue:  # MUST CHANGE THE VALUES WITHIN THE LINK TO MATCH SPREADSHEET (MIN LONG, MIN LAT, MAX LONG, MAX LAT)
        link = requestLink + str(coordmatrix[0, startValue]-0.0005) + "%2C" + str(coordmatrix[1, startValue]-0.0005) + "%2C" + str(coordmatrix[0, startValue]+0.0005) + "%2C" + str(coordmatrix[1, startValue]+0.0005) + "&bboxSR=4326&size=&imageSR=4326&time=&format=jpg&pixelType=U8&noData=&noDataInterpretation=esriNoDataMatchAny&interpolation=+RSP_BilinearInterpolation&compression=&compressionQuality=&bandIds=&sliceId=&mosaicRule=&renderingRule=&adjustAspectRatio=true&validateExtent=false&lercVersion=1&compressionTolerance=&f=image"
        thread = threading.Thread(target=getRequest, args=(link, imageDir, startValue))
        thread.start()
        time.sleep(0.075)
        if startValue % 1000 == 0:
            t1 = time.time()
            print(startValue/(t1-t0))
        startValue += 1

threads = []*4
i = 0
for thread in threads:
    thread = multiprocessing.Process(target=matrixCreation, args=(i))
    thread.start()
    i += 1
for thread in threads:
    thread.join()

t0 = time.time()
getImagesThreaded(0, len(data.index))