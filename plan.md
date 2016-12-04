#The Plan

##Overview of Architecture
We will use PySpark for all processing and Hive for data storage.  The Hive data store will be on AWS.  Initial processing will be conducted locally by the analyst, storing the data in the Hive database for other users.  All code will be store remotely on GitHub.

##Data Gathering Plan
For this analysis, the basic unit (row) will be a <a href="https://www.census.gov/geo/reference/zctas.html">Zip Code Tabulated Area</a>.  ZCTAs are approximately the same as zip codes; however, they have been adjusted to map to actual geographic locations (many zip codes are for commercial locations and PO Boxes only).  Specifically, we will use 2010 ZCTAs rather than 2000.  The Census Bureau provides population and income information for each ZCTA as well as a geocoded location.  This has already been uploaded into the rawdata folder as CSV.
t
Additionally, the census bureau provides lists of urban areas.  We will limit our analysis to urban areas with over 100,000 people.  There over over 300 cities that meet this criteria.  Most importantly, this provides geocoded information for city locations.  This is in the rawdata folder.

The first step is to determine which ZCTAs could be part of which urban areas.  Any ZCTA area within 75 (subject to change) miles of an urban along a great circle will be part of the distance dataset.  We have all of the geocoded data for each ZCTA and urban area, so the distance for all 30,000 x 300 areas should be calculated.  The distance can be calculated using the Law of Haversines (https://en.wikipedia.org/wiki/Haversine_formula).  All distances should be stored in a table in our Hive database.  Any pair of ZCTA and urban area that meets the distance criteria should be stored in a second table.

The next step is to turn all of the "as the crow flies" distances into travel distances.  For this, we will use the Bing Maps Web Service with a REST API (https://msdn.microsoft.com/en-us/library/ff701713.aspx).  Specifically, the guide to get a route is in: https://msdn.microsoft.com/en-us/library/ff701717.aspx.  Whoever works on this will need a Microsoft Account and register for an education key (https://www.microsoft.com/maps/create-a-bing-maps-key.aspx).  We are limited to 125,000 web requests using the educational license, although we can each get one if we need if it is required.  This should by done in Spark using Python and storing the distances in another table in Hive.  Here is a resource on using REST APIs in Python (https://realpython.com/blog/python/api-integration-in-python/).
####Note: Ensure that we save all raw returns from Bing Maps as part of our dataset and not only the final travel distance.

##Analysis Plan
In parallel, someone can develop a model a range dependent model for the number of commuters.  This will need to account for the fact that the a given ZCTA may be close to multiple urban areas (think New York and Newark).  Given this model the commuting-related miles can get calculated on a per-capita basis per ZCTA.

Next, multiple carbon tax models need to be developed.  At a minimum, an uncompensated carbon tax at Kyoto protocols (http://www.ipcc.ch/ipccreports/tar/wg3/index.php?idp=3) will be considered, as well as a compensated carbon tax similar to Washington State's rejected Initiative 732 (https://en.wikipedia.org/wiki/Washington_Initiative_732).  The impact of the taxes will be looked at from both a raw impact and as a percentage of income.

##Visualization Plan
This is highly visual information with geocoded data, so it is an excellent candidate for visualization.  We also need to aggregate on a state level the impact.
