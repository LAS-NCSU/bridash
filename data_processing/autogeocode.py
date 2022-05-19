# Project: LAS - BRI Impact on Local Populations & Sentiment Analysis
# Author: Natalie Kraft
# Purpose: to provide consistency in geocoding across entities - expenditures,
# confucious institutes, natural resources, etc - we can document one script for the generation of
# geocoded entities

import pandas as pd
import geopandas as gpd
import sys
import numpy as np
import reverse_geocoder as rg
import requests

# pattern matches to parse strings
import regex as re

# ensures valid encodings are being used for API calls to OSM
import unicodedata
from unicodedata import normalize

test = False
force_points = False


# checks to see if the city in question exists
# city: a string of the city name to search for
# country: a string of the country name to search for
# cities_df: existing representation of the cities entities to match
# returns -1 if it doesn't exist, if it does, returns the id of the city entity
def loc_exists(loc_name, country, loc_df):
    existing = loc_df.loc[(loc_df['country'] == country) & (loc_df['name'] == loc_name)].reset_index()
    if (len(existing) > 0):
        return [existing['id'][0], existing['country_id'][0]]
    else:
        return [-1]


# looks for a city based on its coordinates
# lat: a float representation of the latitude of a location
# long: a float representation of the longitude of a location
# cities_df: existing representation of the cities entities to match
# returns -1 if it doesn't exist, if it does, returns the id of the city entity
def find_coordinates(lat, long, cities_df):
    error = .005
    sample = cities_df.loc[(cities_df['latitude'] > lat - error) & (cities_df['latitude'] < lat + error) &
                           (cities_df['longitude'] > long - error) & (
                                       cities_df['longitude'] < long + error)].reset_index()
    if len(sample) >= 1:
        print("\tfound " + str(sample['name'].iloc[0]) + " with id " + str(sample['id'].iloc[0]))
        return [sample['name'].iloc[0], sample['id'].iloc[0], sample['country_id'].iloc[0]]
    else:
        return [-1]


# AKA Reverse Geocoding - takes a point and finds the nearest city
# note: this can be somewhat innaccurate
# lat: latitude coordinate
# long: longitude coordinate
# return the string "Dallas, Texas" for location near the coordinates
def find_nearby_city(lat, long, level):
    g = rg.search((lat, long))
    try:
        if level == 'region':
            name = g[0]['admin1']

        if (level == 'city') or (name == ''):
            name = g[0]['name']
        cc = g[0]['cc']
    except:
        print(g)
        return "none identified"

    return name + ", " + cc


# each country is assigned a unique id, this method returns that id given the country name as a string
# country: string representation of the country to retrieve
# country_df : country dataframe containing the ids of countries
def get_country_id(country, country_df):
    try:
        return country_df[country_df['country'] == country]['country_id'].values[0]
    except:
        # If there is difficulty locating it, a "Non" string will be returned.
        # This will not restrict other processes, so pay attend to the print error alert
        print("\tThis country " + str(country) + " was not found")
        return -1

    # this method is used to get the next ID for a city in the given country


# this DOES NOT check to see if that city already exists
# country: string of country
# loc_df: dataframe of cities/regions to check for the next id in
# country_df: dataframe of countries to identify
# returns the id (as a string) for the city/region record to be logged with
def add_next_loc(country, loc_df, country_df):
    # restrict to that country
    limit = loc_df[loc_df['country'] == country]
    # sort the data by the id to find the next id code to use
    limit.sort_values(by='id')

    try:
        # if you cannot grab the last value, then this country has no associated data, start counting at 1
        last_id = limit['id'].iloc[-1]
        country_id = limit['country_id'].iloc[-1]
    except:
        last_id = 0
        country_id = get_country_id(country, country_df)

    if country_id != -1:
        return [last_id + 1, country_id]
    else:
        return [-1]


# utilizes your security credentials to grab the data from S3
# data_needed: string referenceing the type of geocoding completed
#              "city" --> country and cities needed
#              "region" --> country and regions needed
# security_credential_path: absolute path for a .txt file containing your security credentials to read/write data
# from S3
#               read: provided through file path to files needed
#               write: provided through your user secret key
# return the geocoded files
def grab_geocoded_files(type):
    print("Loading geocoded location entities.")
    df = pd.read_csv("../data_final/" + type + ".csv")
    return df

    # return geocoded files in format (country, other)


def write_geocoded_files(data_needed, security_credential_path):
    print("Exporting modified data to geocoded location entities.")
    data_needed.to_csv(security_credential_path, index=False)
    # return geocoded files in format (country, other)


# takes a df - geocoded listing of lat/long coordinates - and pairs it with the associated geocoded entity
# id: string of the column name representing a unique object identifier, used to create the object geocoding mapping
# lat: string of the column name representing the latitude coordinate
# long: string of the column name representing the longitude coordinate
# df: geocoded listing of lat/long coordinates
# return: dataframe representing a map between df[id] and geocode
def coordinates(id_col_name, naming_city, country_col_name, df):
    print("You are reverse geocoding cities. Begin geocoding.")

    # this mapping will store a representation between the id of the project entity and the geocode
    id_mapping = pd.DataFrame(columns=[id_col_name, 'city_temp_id', 'country_id'])

    # pull data from S3
    #   country: dataframe pullesd from S3 denoting country locations (multipolygon geometry)
    #   city: dataframe pulled from S3 denoting city locations (point geometry)
    cities = grab_geocoded_files("cities")
    countries = grab_geocoded_files("countries")

    # geocode
    #   check to see if the city exists
    #   create new entities if the city doesn't exist
    #   update S3 with new references
    for i in range(0, len(df)):

        # print("geocoding: " + str(df[naming_city][i]) + " for " + str(df[id_col_name][i]))
        lat = df['latitude'][i]
        long = df['longitude'][i]
        found = find_coordinates(lat, long, cities)

        if found[0] != -1:
            df[naming_city][i] = found[0]
            id_mapping = id_mapping.append(
                {id_col_name: df[id_col_name][i], 'city_temp_id': found[1], 'country_id': found[2]}, ignore_index=True)
            continue
        else:
            # we need to generate a new city location
            # the naming convention for the location will be prioritized as:
            # 1) an existing city location name
            # 2) a unique name established in the naming_city column of the df established by the caller
            # 3) the project id followed by "near city, country"
            if str(df[naming_city][i]) == "nan":
                df[naming_city][i] = str(df[id_col_name][i]) + " near " + find_nearby_city(lat, long, 'city')

            # generate the id needed for the city
            # we already have the lat/long coordinates to make a point and the name/country, we need the unique id.
            new_id = add_next_loc(df[country_col_name][i], cities, countries)

            # now we can make the point and add it to the cities dataframe right away, this way we can use it for future geocoding
            if new_id[0] != -1:
                cities = cities.append({"name": df[naming_city][i], "id": new_id[0], 'country_id': new_id[1],
                                        "country": df[country_col_name][i], "latitude": lat, "longitude": long},
                                       ignore_index=True)
                # add this new city id to our mapping
                id_mapping = id_mapping.append(
                    {id_col_name: df[id_col_name][i], 'city_temp_id': new_id[0], 'country_id': new_id[1]},
                    ignore_index=True)
            else:
                print("\tThe country " + df[country_col_name][i] + " will not be added to the listing.")

    # export mapping between geocoded entities id and dataframe ids
    print("Exporting new cities to database")

    if test == True:
        write_geocoded_files(cities, "../data_final/citiestest.csv")
    else:
        write_geocoded_files(cities, "../data_final/cities.csv")

    # return mapping between geocoded entities id and dataframe ids
    return id_mapping


# takes a df without location entities and pairs it with the associated geocoded entity
# id_col_name: string of the column name representing a unique object identifier, used to create the object geocoding mapping
# country_col_name: string of the column name representing the country
# df: geocoded listing of locations to geocode at the country level
# return: dataframe representing a map between df[id] and geocode
def country_geocoding(id_col_name, country_col_name, df):
    print("You are geocoding entities at the country level. Begin geocoding.")

    # pull data from S3
    #   country: dataframe pulled from S3 denoting country locations (multipolygon geometry)
    countries = grab_geocoded_files("countries")[['country', 'country_id']]

    # pair all instances of a country with the country id from our location entity file
    df = df.merge(countries, left_on=country_col_name, right_on="country", how="left")

    # remove any instances where the country_id is null, indicating a country has not been found
    # reduce the information to only the mapping required
    id_mapping = df[df['country_id'].notna()][[id_col_name, "country_id"]]

    # no need to export new locations as all countries have a fixed listing
    # return mapping between geocoded entities id and dataframe ids
    return id_mapping


# takes a df - listing of regions and countries - and pairs it with the associated geocoded entity
# id_col_name: string of the column name representing a unique object identifier, used to create the object geocoding mapping
# region_col_name: string of the column name representing the region
# country_col_name: string of the column name representing the country
# df: geocoded listing of regions and countries
# return: dataframe representing a map between df[id] and geocode
def geocoding(id_col_name, loc_col_name, country_col_name, df, level):
    print("You are geocoding " + level + ". Begin geocoding.")
    # this mapping will store a representation between the id of the project entity and the geocode
    key = level + '_temp_id'
    id_mapping = pd.DataFrame(columns=[id_col_name, key, 'country_id'])

    # pull data from S3
    #   country: dataframe pulled from S3 denoting country locations (multipolygon geometry)
    #   region: dataframe pulled from S3 denoting city locations (multipolygon geometry)
    locs = grab_geocoded_files(level)
    countries = grab_geocoded_files("countries")

    # remove any special characters for the naming conventions of all objects passed in

    # geocode
    #   check to see if the region exists
    #   create new entities if the region doesn't exist
    #   update S3 with new references
    for element in range(0, len(df)):
        loc_name = df[loc_col_name][element]
        country_name = df[country_col_name][element]
        id_name = df[id_col_name][element]

        id = loc_exists(loc_name, country_name, locs)
        if id[0] != -1:
            # the region has been found
            # print("The region " + str(element) + " has been found")
            id_mapping = id_mapping.append({id_col_name: id_name, key: id[0], "country_id": id[1]}, ignore_index=True)

        else:
            # print("The region " + str(loc_name) + " has not been found, generating new region now")
            # we must create a new entity
            # try to grab the region with the region/country names
            search_term = loc_name.strip().replace(" ", "+")
            country_term = country_name.replace(" ", "+")
            search_term = normalize('NFKC', ''.join(
                c for c in normalize('NFKD', search_term) if unicodedata.category(c) != 'Mn'))
            
            try: 
                query_f = gpd.read_file(
                    # use "&country=" to search the country specifically 
                "https://nominatim.openstreetmap.org/search?q=" + search_term + "%2C+" + country_term + "&format=geojson&polygon_geojson=1")
                
                if len(query_f) == 0: 
                    # try without the country identifier
                    query_f = gpd.read_file("https://nominatim.openstreetmap.org/search?q=" + search_term + "&format=geojson&polygon_geojson=1")
           
            except: 
                print("a service error has occured when retrieving this file from OSM.")
            # if we found an entry, grab the highest ranking entity out of all the regions identified
            # also restrict for the type of shape we are expecting. Cities expects a point, regions expects a Polygon.
            typ = {
                "regions": "Polygon",
                "cities": "Point"
            }

            query = query_f[query_f['geometry'].type == typ[level]].reset_index()
            #if (len(query) == 0) & (level == "cities") & force_points:
            if force_points:
                query_f['geometry'] = [x.centroid if x.area < .1 else x for x in query_f['geometry'] ]
                query = query_f[query_f['geometry'].type == typ[level]].reset_index()

            if len(query) > 0:
                g = query.iloc[0]['geometry']
                # print(loc_name + " is being added to the bank of locations")

                # generate a new location id
                new_id = add_next_loc(country_name, locs, countries)

                if new_id[0] != -1:
                    # add the location to the regions dataframe right away, to ensure no duplicate entries are written
                    if level == 'cities':
                        locs = locs.append(
                            {"name": loc_name, "id": new_id[0], "country_id": new_id[1], "country": country_name,
                             "latitude": g.y, "longitude": g.x}, ignore_index=True)
                    else:
                        locs = locs.append(
                            {"name": loc_name, "id": new_id[0], "country_id": new_id[1], "country": country_name,
                             "geometry": g}, ignore_index=True)
                        # add this new region id to our mapping
                    id_mapping = id_mapping.append({id_col_name: id_name, key: new_id[0], "country_id": new_id[1]},
                                                   ignore_index=True)
                else:
                    print("Location " + country_name + " not added to mapping or location entities.")
            else: 
                print("Not found: " + loc_name)

    # export the new locations dataframe
    print("Exporting new " + level + " to database")

    if test == True:
        write_geocoded_files(locs, "../data_final/" + level + "test.csv")
    else:
        write_geocoded_files(locs, "../data_final/" + level + ".csv")

    # return mapping between geocoded entities id and dataframe ids
    return id_mapping


if __name__ == "__main__":
    __spec__ = None

    # TODO: add in argparser https://realpython.com/command-line-interfaces-python-argparse/

    # grab geocoded files from S3

    # identify the type of geocoding the file needs
    # previously seen:
    #       - coordinates (lat/long) --> reverse geocoding and matching with base
    #       - city, countries --> geocoding
    #       - admin boundaries --> geocoding --> parsing with

    # system arguments include
    # 1: file path to geocode
    # 2: type of geocoding - {C: coordinates, gl3: geocoding of cities, gl2: geocoding of regions}
    # 3/4/5: column headers for the file for:
    #       C: optional_naming_for_city country id
    #       gl3: city country id
    #       gl2: region country id
    #       gl1: country country id
    # 6: optional file to only test output
    # Unused: security credentials to access S3 for reading/writing geocoding data files

    print("Preparing system configuration.")
    param = "(\"" + sys.argv[5] + "\", \"" + sys.argv[3] + "\", \"" + sys.argv[4] + "\", geocoding_df"
    type = {
        "C": "coordinates" + param + ")",
        "gl3": "geocoding" + param + ", \"cities\")",
        "gl2": "geocoding" + param + ", \"regions\")",
        "gl1": "country_geocoding" + "(\"" + sys.argv[5] + "\", \"" + sys.argv[3] + "\", geocoding_df)"
    }

    func = type.get(sys.argv[2], "print(\"You have chosen an invalid geocoding scheme.\") return \"Failure\"")

    if len(sys.argv) >= 7 and sys.argv[6] == 'force':
        force_points = True

    if len(sys.argv) == 8 and sys.argv[7] == 'test':
        test = True

    print("Loading file to geocode")
    geocoding_df = pd.read_csv(sys.argv[1])

    exec("mapping = " + func)

    print("Exporting mapping results.")
    mapping.to_csv(sys.argv[1].rsplit(".", 1)[0] + "_results.csv", index=False)

    print("Geocoding complete.")