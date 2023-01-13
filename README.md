# Crevasse

Created by Luke Steinbicker, Andrew Norway <br/>
Contact us at main@crevasse.org to look at our full codebase or download our network. <br/>

## Building Classifier

A frequent problem in developing nations without extensive public records is the identification of building types within a city. By training a neural network using millions of high resolution aerial images, we aim to combat this challenge and enable the rapid categorization of structures within a city.

### Methodology

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/121472675/212436048-cd8d75cb-90dc-48a8-8df3-e9c683b16ecb.png">
  <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/121472675/212436057-cc70f600-db80-46d2-ab66-8757cb889b9f.png">
  <img alt="Layout" src="https://user-images.githubusercontent.com/121472675/212436048-cd8d75cb-90dc-48a8-8df3-e9c683b16ecb.png">
</picture>

### Data Sources
Columbus, OH: <br/>
Parcel Information- https://opendata.columbus.gov/datasets/columbus::address-points-1 <br/>
Imagery- https://maps.columbus.gov/arcgis/rest/services/Imagery/Imagery2021/MapServer <br/>
Chicago, IL: <br/>
Parcel Information- https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Parcel-Universe/tx2p-k2g9/data <br/>
Imagery- https://gis.cookcountyil.gov/imagery/rest/services/CookOrtho2021/ImageServer <br/>
Los Angeles, CA: <br/>
Parcel Information- https://geohub.lacity.org/datasets/6d85cb5f5f5641c6aa95203849ca05bb_0 <br/>
Imagery- https://cache.gis.lacounty.gov/cache/rest/services/LACounty_Cache/LACounty_Aerial_2014/MapServer <br/>
Wilmington, NC: <br/>
Parcel Information- https://www.nconemap.gov/datasets/nconemap::north-carolina-parcels-centroids <br/>
Imagery- https://services.nconemap.gov/secure/rest/services/Imagery/Orthoimagery_Latest/ImageServer <br/>
Winston Salem, NC: <br/>
Parcel Information- https://www.nconemap.gov/datasets/nconemap::north-carolina-parcels-centroids <br/>
Imagery- https://services.nconemap.gov/secure/rest/services/Imagery/Orthoimagery_Latest/ImageServer <br/>
Greensboro, NC: <br/>
Parcel Information- https://www.nconemap.gov/datasets/nconemap::north-carolina-parcels-centroids <br/>
Imagery- https://services.nconemap.gov/secure/rest/services/Imagery/Orthoimagery_Latest/ImageServer <br/>
Washington, DC: <br/>
Parcel Information- https://opendata.dc.gov/datasets/DCGIS::existing-land-use <br/>
Imagery- https://imagery.dcgis.dc.gov/dcgis/rest/services/Ortho/Ortho_2021/ImageServer <br/>
