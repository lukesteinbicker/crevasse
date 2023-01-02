import pandas as p
import numpy
import requests
import threading

data = p.read_excel("C:/Users/lukes/Desktop/Project/Backend/DC/DCFullPropertiesDataFinal.xlsx", usecols='A:D', header=0)
numrows = len(data.index)
rowvalue = 0
n = 50 #number of threads
imagerylink1 = "https://imagery.dcgis.dc.gov/dcgis/rest/services/Ortho/Ortho_2021/ImageServer/exportImage?bbox=" #imagery link up to bbox=
imagerylink2 = "&bboxSR=4326&size=&imageSR=4326&time=&format=jpg&pixelType=U8&noData=&noDataInterpretation=esriNoDataMatchAny&interpolation=+RSP_BilinearInterpolation&compression=&compressionQuality=&bandIds=&sliceId=&mosaicRule=&renderingRule=&adjustAspectRatio=true&validateExtent=false&lercVersion=1&compressionTolerance=&f=image"
imagerypath = "C:/Users/lukes/Desktop/Project/Images/ImageBin/"

coordmatrix = numpy.empty((6, numrows))

while rowvalue < numrows:
    coordmatrix[0, rowvalue] = data.iloc[rowvalue, 3] - 0.0005 #minlong
    coordmatrix[1, rowvalue] = data.iloc[rowvalue, 3] + 0.0005 #maxlong
    coordmatrix[2, rowvalue] = data.iloc[rowvalue, 2] - 0.0005 #minlat
    coordmatrix[3, rowvalue] = data.iloc[rowvalue, 2] + 0.0005 #maxlat
    coordmatrix[4, rowvalue] = data.iloc[rowvalue, 1] #use code
    coordmatrix[5, rowvalue] = rowvalue #row number
    rowvalue += 1

coordmatrixsplit = numpy.array_split(coordmatrix, n, axis=1)

def myfunction(coordm0, coordm1, coordm2, coordm3, coordm4, coordm5):
    y = 0
    while y <= len(coordm5):
        link = imagerylink1 + str(coordm0[y]) + "%2C" + str(coordm2[y]) + "%2C" + str(coordm1[y]) + "%2C" + str(coordm3[y]) + imagerylink2
        req = requests.get(link, allow_redirects = True)
        name = imagerypath + str(coordm5[y]) + "_" + str(coordm4[y]) + ".jpg"
        open(name, 'wb').write(req.content)
        y += 1

n = n - 1

while n > 0:
    t = threading.Thread(target=myfunction, args=(coordmatrixsplit[n][0], coordmatrixsplit[n][1], coordmatrixsplit[n][2], coordmatrixsplit[n][3], coordmatrixsplit[n][4], coordmatrixsplit[n][5]))
    t.start()
    n -= 1