# Confucius Institute Dataset Guide

Confucius institutes can be found in the data_final folder under [confucius_insititutes.csv](../data_final/confucius_institutes.csv). 

# Dataset Column Definitions

### Structure for Global Listing of Confucius Institutes
**file name:** [confucius_insititutes.csv](../data_final/confucius_institutes.csv)


|Field Name|	Description|
|---|---|
| id	| This field provides the unique identification number for each Confucius Institute. |
| confucius_institute	| Name of the Confucius Institute that has been established. |
| partner_uni | The university based in China that a domestic institution has partnered with to host a Confucius Institute. If the Chinese partner university was not able to be found, it is labeled "Unknown". International universities do not have a partner university. |
| date_est	| Estimated established date. |
| location_name | Location name used to log CI location through OSM. | 
| nearest_city | Preliminary processing of this dataset outputted a city that the CI was near. This city was not used as the primary method of geocoding, but is retained for readability & interpretability of dataset. *Do NOT use this column for geocoding, see gl3_id* | 
| country | Country the host univeristy is located. | 
| status | Flag indicating if the Confucius Institute is open or closed as of 4/22/22. *Based on checking availability of known ci_webpage* | 
| ci_webpage | Website identified for the Confucius Institute. | 
| sources | Websites with information about CI. Not considered a *homepage* but still has relevant information. | 
| gl3_id | This field provides a more granular view on the CI location. Geocode level 3 looks specifically at cities.  It pairs with a city dataframe, which includes longitude/latitude coordinates for the cities as well as city statistics. | 
| country_id | This field provides a three digit code for countries. It pairs with the country dataframe, which logs the shapefile for the country as well as country level statistics. | 

*Note: We are looking to improve the accuracy of this data by filling the date established field and creating a closing date for the university to increase accuracy.* 


# Other raw datasets (not-geocoded) 

Confucius Institutes have been compiled originally in two datasets:
- a collection of all institutes in the United States [(_usa_ci.csv_)](../data_processing/confucius_institutes/usa_ci.csv)
- a collection of all institues across the rest of the world, excluding the United States [(_international_ci.csv_)](../data_processing/confucius_institutes/international_ci.csv)

This data was compiled into one running list and then geocoded. 

### Structure for Confucius Institutes in the USA
**file name:** [(_usa_ci.csv_)](../data_processing/confucius_institutes/usa_ci.csv)

|Location|Partner Uni|Country|index|Status|
|--------|-----------|------|------|------|
|Location of the Confucius Institute within the United States. Institutes are typically hosted at a college univeristy, equivalent educational school system, or school district|The university based in China that a domestic institution has partnered with to host a Confucius Institute. If the Chinese partner university was not able to be found, it is labeled "Unknown"|Country the host univeristy is located. For this dataset, the Country is always USA. This column is used for geocoding.|Numeric label used for geocoding.|Flag indicating if the Confucius Institute is open or closed as of 4/22/22.|

### Structure for International Confucious Institutes
**file name:** [(_international_ci.csv_)](../data_processing/confucius_institutes/international_ci.csv)

|index|Country|Confucius Institute|Location|Status|
|--------|-----------|------|------|------|
|Numeric label used for geocoding.|Country the host univeristy is located.|Official name of the Confucius Institute|Location of the international Confucius Institute. Institutes are typically hosted at a college univeristy, equivalent educational school system, or school district|Flag indicating if the Confucius Institute is open or closed as of 4/22/22.|

# Dataset Sources
The dataset of US Confucius Institutes are based on the lists from the following sources:
- [Washington Examiner: China on campus: Confucius Institutes collapse nationwide](https://www.washingtonexaminer.com/news/confucius-institutes-collapse-us-campuses)
- [National Association of Scholars: How Many Confucius Institutes Are in the United States?](https://www.nas.org/blogs/article/how_many_confucius_institutes_are_in_the_united_states)

The dataset of International Confucius Institutes are scraped from the following website:
- [Dig Mandarin: Confucius Institutes Around the World – 2021](https://www.digmandarin.com/confucius-institutes-around-the-world.html)

# Dataset Processing Methodology 
- **'Confucius Institute' Column:** Names of institutes were scraped using the _Beautiful Soup_ Python Library
- **'Location' Column:** The educational institution associated with a Confucius Institute was parsed out of the 'Confucius Institute' column using regex. If OpenStreetMap could not identify the name location of the university, the location field is broadened to a district/city manually.
- **'Status' Column:** A Confucius Institute was determined to be Open or Closed based on the the website. If a website has been taken down, we assume the Confucius Institute has been closed. If the website is active, we scrape the website for keywords indicating whether the institute is closed or not. The pseudocode below outlines the python script used to generate the 'status' column: 
```
For each website in csv:
  
  Get HTTP status_code using urllib.request('link')
  if status_code == 200:
    # Website is active, scrape for keywords
    Using Beautiful Soup, scrape all text off of the website.
    
    if text contains any of the keywords ['does not exist', '404', 'closed', 'closing', 'close', 'shut down', 'transferred']:
      status = 'Closed'
    else:
      status = 'Open'
    
  else:
    # Website is inactive, assume institute is closed
    status = 'Closed'
```

Original data scraped from sources [here](../data_processing/confucius_institutes/ci_exploration/Location_Validaiton.ipynb). 

Geocoding of dataset (and final cleaning) was computed [here](../data_processing/confucius_institutes/ci_processing.ipynb). 
