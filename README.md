# Crevasse

Created by Luke Steinbicker, Andrew Norway <br/>
Contact us at main@crevasse.org to look at our full codebase or download our network. <br/>

## Building Classifier - Estimated to Release by March 1, 2023

Building detection methods are already well-developed, but developing a way to discern intended building use poses a unique challenge. We aim to train a neural network using millions of high resolution aerial images, enabling the rapid categorization of structures within an area.

### Simplified Methodology

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/121472675/212436048-cd8d75cb-90dc-48a8-8df3-e9c683b16ecb.png">
  <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/121472675/212436057-cc70f600-db80-46d2-ab66-8757cb889b9f.png">
  <img alt="Layout" src="https://user-images.githubusercontent.com/121472675/212436048-cd8d75cb-90dc-48a8-8df3-e9c683b16ecb.png">
</picture>

### Data Sources
- Boston, MA <br/>
  - https://dataverse.harvard.edu/file.xhtml?fileId=6416148&version=1.0 <br/>
  - https://tiles.arcgis.com/tiles/hGdibHYSPO59RG1h/arcgis/rest/services/orthos2021/MapServer <br/>
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
- Buffalo, NY <br/>
  - https://data.buffalony.gov/Government/Current-Assessment-Roll-2022-2023-/4t8s-9yih <br/>
  - https://gis.buffalony.gov/server/rest/services/Hosted/Buffalo2021/MapServer <br/>
- Phoenix, AZ <br/>
  - https://koordinates.com/layer/111362-maricopa-county-arizona-parcels/ <br/>
  - https://gis.mcassessor.maricopa.gov/arcgis/rest/services/Aerials2022/MapServer <br/>
- Seattle, WA <br/>
  - https://gis-kingcounty.opendata.arcgis.com/datasets/parcels-for-king-county-with-address-with-property-information-parcel-address-area/explore <br/>
  - https://gismaps.kingcounty.gov/arcgis/rest/services/BaseMaps/KingCo_Aerial_2021/MapServer <br/>
- Alameda, CA <br/>
  - https://data.acgov.org/datasets/b55c25ae04fc47fc9c188dbbfcd51192_0/explore <br/>
  - https://tiles.arcgis.com/tiles/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/Aerial_Imagery_2017/MapServer <br/>
- Philadelphia, PA <br/>
  - https://www.opendataphilly.org/dataset/opa-property-assessments <br/>
  - https://tiles.arcgis.com/tiles/fLeGjb7u4uXqeF9q/arcgis/rest/services/CityImagery_2020_3in/MapServer <br/>
- Miami, FL <br/>
  - Requested from Miami GIS <br/>
  - https://imageserverintra.miamidade.gov/arcgis/rest/services/WGS1984_WebMercator/2021_Woolpert_WGS1984_WebMercator/ImageServer <br/>
