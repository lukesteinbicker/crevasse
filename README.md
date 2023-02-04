# Crevasse

Created by Luke Steinbicker, Andrew Norway <br/>
Contact us at main@crevasse.org to look at our full codebase or download our network. <br/>

## Building Classifier

A frequent problem in developing nations without extensive public records is the identification of building types within a city. By training a neural network using millions of high resolution aerial images, we aim to combat this challenge and enable the rapid categorization of structures within a city.

### Simplified Methodology

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/121472675/212436048-cd8d75cb-90dc-48a8-8df3-e9c683b16ecb.png">
  <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/121472675/212436057-cc70f600-db80-46d2-ab66-8757cb889b9f.png">
  <img alt="Layout" src="https://user-images.githubusercontent.com/121472675/212436048-cd8d75cb-90dc-48a8-8df3-e9c683b16ecb.png">
</picture>

### Data Sources
- Boston, MA <br/>
  - https://dataverse.harvard.edu/file.xhtml?fileId=6416148&version=1.0 <br/>
  - https://tiles.arcgis.com/tiles/hGdibHYSPO59RG1h/arcgis/rest/services/orthos2021/MapServer?f=html&cacheKey=a5b526e09d4312d2 <br/>
- New York, NY <br/>
  - https://data.cityofnewyork.us/City-Government/Primary-Land-Use-Tax-Lot-Output-PLUTO-/64uk-42ks/data <br/>
  - https://orthos.its.ny.gov/arcgis/rest/services/wms/2022/MapServer <br/>
- Chicago, IL <br/>
  - https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Parcel-Universe/tx2p-k2g9/data <br/>
  - https://gis.cookcountyil.gov/imagery/rest/services/CookOrtho2021/ImageServer <br/>
- Los Angeles, CA <br/>
  - https://geohub.lacity.org/datasets/6d85cb5f5f5641c6aa95203849ca05bb_0 <br/>
  - https://cache.gis.lacounty.gov/cache/rest/services/LACounty_Cache/LACounty_Aerial_2014/MapServer <br/>
- Washington, DC <br/>
  - https://opendata.dc.gov/datasets/DCGIS::existing-land-use <br/>
  - https://imagery.dcgis.dc.gov/dcgis/rest/services/Ortho/Ortho_2021/ImageServer <br/>
