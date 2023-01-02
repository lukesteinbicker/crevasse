import pandas as p
import numpy
import requests
import threading

data = p.read_csv("PATHHERE", usecols=[], header=0)
numrows = len(data.index)
rowvalue = 0 #row, zero indexed
longcol = 0 #longitude column, zero indexed
latcol = 1, #latitude column, zero indexed
usecodecol = 2 #use code column, zero indexed
n = 50 #number of threads
imagerylink1 = "LINK UP TO bbox=" #imagery link up to bbox=
imagerylink2 = "&bboxSR=4326&size=&imageSR=4326&time=&format=jpg&pixelType=U8&noData=&noDataInterpretation=esriNoDataMatchAny&interpolation=+RSP_BilinearInterpolation&compression=&compressionQuality=&bandIds=&sliceId=&mosaicRule=&renderingRule=&adjustAspectRatio=true&validateExtent=false&lercVersion=1&compressionTolerance=&f=image"
imagerypath = "PATHHERE" #directory to store download images in

coordmatrix = numpy.empty((4, numrows))

while rowvalue < numrows:
    coordmatrix[0, rowvalue] = data.iloc[rowvalue, longcol]
    coordmatrix[1, rowvalue] = data.iloc[rowvalue, latcol]
    coordmatrix[2, rowvalue] = data.iloc[rowvalue, usecodecol]
    coordmatrix[3, rowvalue] = rowvalue
    rowvalue += 1

coordmatrixsplit = numpy.array_split(coordmatrix, n, axis=1)

def myfunction(coordm0, coordm1, coordm2, coordm3):
    y = 0
    while y <= len(coordm3):
        link = imagerylink1 + str(coordm0[y] - 0.0005) + "%2C" + str(coordm1[y] - 0.0005) + "%2C" + str(coordm0[y] + 0.0005) + "%2C" + str(coordm1[y] + 0.0005) + imagerylink2
        req = requests.get(link, allow_redirects = True)
        name = imagerypath + str(coordm3[y]) + "_" + str(coordm2[y]) + ".jpg"
        open(name, 'wb').write(req.content)
        y += 1

n = n - 1

while n > 0:
    t = threading.Thread(target=myfunction, args=(coordmatrixsplit[n][0], coordmatrixsplit[n][1], coordmatrixsplit[n][2], coordmatrixsplit[n][3]))
    t.start()
    n -= 1