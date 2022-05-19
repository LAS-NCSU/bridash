## Geocoding Conventions 

Every data entity will have a coded location entity. More specifically, data entries (expenditures, public opinion, natural resources, confucious institutes, etc) will all have three shared data fields to allow geocoding: level 1: countries, level 2: regions, and level 3: cities. There will always be a country id present, depending on the granularity of the location information available, regional and/or city data may be available. 

### Data Storage & Access

The location data is located in S3. There are three data tables you need to have access to: 
- country (multipolygons)
- regional (multipolygons)
- city (point) 

The data is stored on S3. To access the datasets, you can copy the file within your terminal

```
# --no-sign-request is only needed if you have a LAS AWS account 
% aws --no-sign-request s3 cp s3://las.bri.public/27803y98ul/countries.csv .
% aws --no-sign-request s3 cp s3://las.bri.public/27803y98ul/regions.csv .
% aws --no-sign-request s3 cp s3://las.bri.public/27803y98ul/cities.csv .
``` 

At this time, no write access is allowed through the AWS CLI. Visit [LAS' AWS](https://us-east-2.signin.aws.amazon.com/oauth?response_type=code&client_id=arn%3Aaws%3Aiam%3A%3A015428540659%3Auser%2Fs3&redirect_uri=https%3A%2F%2Fs3.console.aws.amazon.com%2Fs3%2Fbuckets%2Flas.bri.public%3Fregion%3Dus-east-1%26state%3DhashArgs%2523%26tab%3Dobjects%26isauthcode%3Dtrue&forceMobileLayout=0&forceMobileApp=0&code_challenge=NY5Zucll4-hHmTpdrMp4oNMfmyBCKKoXGbtfz7um0S8&code_challenge_method=SHA-256) portal to manually upload new location datasets. 

A couple of things to note: 
- regions and cities are datasets that should be updates when any new location is logged 
- countries is a semi-permanent listing of countries. Extreme caution should be used when updating these localities, and a review of other countries locations is needed to update all other data entities to the new scheme if any changes are made. 

### Data Fields 

__Country Data Table__ 
|name|country_id|country|geometry|iso|other_attributes|
|---|---|---|---|---|---|
|United States|001|United States|MultiPolygon(((...)))|US|other_attributes|
|Russia|002|Russia|MultiPolygon(((...)))|RU|other_attributes|

__Regional Data Table__ 
|name|id|country|country_id|geometry|other_attributes|
|---|---|---|---|---|---|
|North Carolina|1|United States|001|MultiPolygon(((...)))|other_attributes|
|Penza|1|Russia|002|MultiPolygon(((...)))|other_attributes|

__Cities Data Table__ 
|name|id|country|country_id|latitude|longitude|other_attributes|
|---|---|---|---|---|---|---|
|Pittsburgh|1|US|001|y|x|other_attributes|
|Moscow|1|Russia|002|y|x|other_attributes|
|St. Petersburgh|002|Russia|2|y|x|other_attributes|

### Geocoding 

The country data was pulled from ArcGIS. This is static information and does not need to be updated. (There is some political disputed territories that could change in the future; currently data is logged with the geographical country in closest proximity and not with a Western/other biased leaning. When pulling in new data, some of their existing notion for country names may be unique. Upon autogeocoding, error messages should flag countries that are not recognized. Utilize this [common mapping dictionary](../data_processing/country_config.txt) to ensure that all of the country naming conventions are identical to the convention laid forth in the countries.csv on S3. 

Regional data was in part generated from GeoAid Data's custom shapefiles provided. If the shapefiles were small in nature (<.01 area), they were converted to a point/city data. 
Larger shapefiles were added to the regional areas.

__Reading in the CSVs__ 

Encoding errors when data is viewed in excel is common. No trouble has been seen when loading the data using pandas. To convert from a csv to a GeoDataFrame for visualizations, you may use the following structure.

For polygons:
```
# convert shapes back to polygons
countries['geometry'] = [shapely.wkt.loads(x) for x in countries['geometry']]
# add into GeoDataFrame 
countries = gpd.GeoDataFrame(countries).reset_index(drop=True))
# merge data on 'country_id'
viz1 = countries.merge(dataset, on='country_id', how='left')
```

For points: 
```
# create the GeoDataFrame with the point coordiante data
cities = gpd.GeoDataFrame(cities, geometry=gpd.points_from_xy(cities['longitude'], cities['latitude']))
# merge in the base data set 
# note: you must use the 'gl3_id' code AND 'country_id' to merge data on
viz1 = cities.merge(ex, left_on=['country_id', 'id'], right_on=['country_id', 'gl3_id'], how='right')
```
As an example of the geocoding scheme, a sample visualization template has been compiled. Visit [financial_viz.ipynb](../data_processing/geoaid/financial_viz.ipynb).

### Sources 

- Country data is sourced from open source [ArcGIS products](https://opendata.arcgis.com/datasets/2b93b06dc0dc4e809d3c8db5cb96ba69_0.geojson).
- Regional data is pulled from OSM. 
- City data is pulled from [Simple Maps](https://simplemaps.com/data/world-cities) and OSM.  
