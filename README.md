# LAS-BRI
This project is a part of the [Laboratory for Analytic Sciences](https://ncsu-las.org) at NC State University. 

## Project Intro

Influence projects focused on identifying and characterizing malign foreign influence campaigns. The Influence team’s efforts this year focused on three distinct but related areas of research. This included efforts on developing capabilities to detect social media influence campaigns, this year with a focus on campaigns that crossed multiple social media platforms (Social Media Influence Campaigns) as well as work on understanding and characterizing economic influence campaigns focused on a country's leadership, also known as elite capture (Economic Investment Influence Campaigns). Additionally, the Influence team researched methods to measure the scope and effectiveness of a foreign influence campaign (Effectiveness Measures for Influence Campaigns). 

This project aims to understand and visualize the complex relationships between Chinese foreign investment, public opinion on Chinese development, and microeconomic features. Focusing on the influence caused by the Belt & Road Initiative, spatiotemporal analysis of institutional strength, standard of living, public opinion and financial expenditures has led to the identification of feature sets indicative of positive and negative sentiment toward China. Our goal is to utilize these feature sets in the predictive modeling of global changes in sentiment to support analysts’ workflow and prioritization of US counter influence efforts. A comparative analysis has been conducted across case study countries - Malaysia, Italy, Sweden, and New Zealand - using logistic regression and random forests for variable identification. Hierarchical clustering is utilized to identify trends within groups of similar perception toward Chinese influence. In support of this line of research, a dashboard prototype is in development to support the analysis of microeconomic indicators, BRI predictive feature sets and public sentiment. We aim to provide these insights to users to interact with and develop rationale for independent case studies to support mission-relevant objectives and support analysts' workflows. This prototype demonstrates the feasibility and promise of continued visualization and modeling of BRI impact globally.

### Methods Used
* Feature Engineering 
* Data Visualization
* Predictive Modeling
* Inferential Statistics
* etc.

### Technologies
* Pandas, scikit-learn, matplotlib, folium
* HTML
* ArcGIS, Experience Builder
* Jupyter Notebooks
* etc. 

## Needs of this project

- geospatial analysis
- data exploration / descriptive statistics
- data processing / cleaning across data sources
- statistical modeling
- machine learning
- automated reporting

## Getting Started

1. Clone this repo (for help see this [tutorial](https://help.github.com/articles/cloning-a-repository/)).
2. Data: 
    a. Entity Raw Data is being kept [here](data_processing) within this repo. Data is separated by data type (ie. financial, public opinion, world statistics, etc). 
    b. Geocoded Data is being stored in S3 and within this repo *all geocoded data shortly to be stored exclusivly in S3*. Three levels of geocoding exist level 1 [countries](data_final/countries.csv), level 2 [regions](data_final/regions.csv), and level 3 [cities](data_final/cities.csv). *See below for the contents and use of geocoded tables.*
    
3. Ongoing methodology for cleaning this data can be found as well. All final preprocessed data is [here](data_final). The structure for transformed data can be found within the [geocoding](data_final/geocode.md) documentation.

All entity data - public opinion, financial expenditures, etc - will be coded with a level 1 (country_id), level 2 (g2_id) and level 3 (gl3_id) id. When utillizing the data in visualizations/modeling, you can pull over attributes of the location via S3 and/or the actual geometries.  You will need to merge the geodata using both level 1 AND (level 2 or level 3) data. 

*The readme also includes documentation on writing new locations to these tables.*

4. All [data exploration](data_exploration) and [modeling](modeling) can be found at the respective links. Further detail about each model's purpose can be found in independant readme's or within a notebook. 

## ArcGIS
It should be noted that this research line supports the continued development of a dashboard highlighting Chinese Influence. The dashboard can be found [here](go.ncsu.edu/las-bri). 

To support the backend development of the dashboard, an ArcGIS account is required. Free licenses are offered to NC State students/faculty/affiliates. You can find additional information about setting up an account [here](https://www.lib.ncsu.edu/gis/arcgisonline). 

*For access to the dashboard data sources and experience builder backend, please contact Natalie Kraft.*

## Featured Notebooks & Deliverables

__Automating Geocoding__ To automate geocoding a new dataset, utilize the [autogeocode](data_processing/autogeocode.py) file. You can pass in a listing of processed data points with some location entity - coordinates or location name - and it will update our final listing of geocoded locations and return a listing of the geocoding locations for every processed data point. 

__Demo geocoding scheme__ To showcase how the geocoding scheme can be processed with any cleaned dataset, check out this [financial expenditure visualizations guide](data_processing/geoaid/financial_viz.ipynb)

__Data Deliverables__ For a full listing of the data processed and geocoded, see [available_data](available_data.md)

### Qualitative Rationale 

For additional resources on the rationale and underlying motivation of this research line, visit the [LAS Influence Team's 2021 Symposium](https://symposium.ncsu-las.net/influence.html). 

## Contributing Members

|Name     |  Email Address  | 
|---------|-----------------|
|Natalie Kraft |   nakraft@ncsu.edu      | 
|Michelle Winemiller |    mawinemi@ncsu.edu   |
|Christine Brugh  |    csbrugh@ncsu.edu  |
|Stephen Shauger |    seshauge@ncsu.edu   |
|Manali Shirsekar |    mnshirse@ncsu.edu  |

## Contact 
* Our slack channel is `#bri-dashboard`
* Feel free to contact Natalie Kraft with any questions or if you are interested in contributing!

