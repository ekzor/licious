## functionality
This script takes in the JSON data from the City of Toronto Summerlicious (or Winterlicious) website and uses a combination of restaurant name and postal code to query Google for review data. the rating comes from the Google Places box that appears on the right side of a Google search.

The City of Toronto data is not included in this repository as it may be copyrighted and I'd rather not find out the hard way. You can get it yourself by going to the API URL at https://secure.toronto.ca/cc_sr_v1/data/SummerRestaurantListJSON/0

## external dependencies
- unicodecsv
- requests

## known issues
- Eggpsectation has multiple locations and, despite specifying the postal code, does not return a Places box. But who cares, it's just Eggpsectation.

## mapped heatmap of the results
https://drive.google.com/open?id=16Pp2jmxH8Nc65IrUFyIHTNnHUbNTVmsS&usp=sharing

## disclaimer
Scraping Google may be against the Google TOS and you do so at your own risk.
