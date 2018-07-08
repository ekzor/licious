import json
import time
import random
from HTMLParser import HTMLParser
import unicodecsv
import requests

class ParseRating(HTMLParser):
  '''HTMLParser class to pull out the data from a <span> with class='rtng'.
  Access the returned data through the 'data' class variable.'''
  
  #class variables
  ratingtag = False
  data = -1
  
  def handle_starttag(self,tag,attrs):
    if tag == 'span' and (u'class',u'rtng') in attrs:
      self.ratingtag = True
      
  def handle_endtag(self,tag):
    if self.ratingtag and tag == 'span':
      self.ratingtag = False
      
  def handle_data(self,data):
    if self.ratingtag:
      self.data = data

#load restaurant data. this is obtained from the summerlicious website's API call: https://secure.toronto.ca/cc_sr_v1/data/SummerRestaurantListJSON/0
#since this data is unlikely to change during the event, it's been saved to a file to avoid from having to pull it every time
inputfile = "2018-summerlicious.json"
with open(inputfile) as f:
    data = json.load(f)

#open a new CSV file based on the input filename and write a header row
with open(inputfile[:inputfile.find(".")]+"_ratings.csv","wb+") as csvfileref:
  csvfile = unicodecsv.writer(csvfileref, encoding='utf-8')
  csvfile.writerow(['name','rating','address','postal code','lat','long','lunch','dinner','menu link'])

  count = 0

  for resto in data["restaurants"]:
    count += 1
    
    #use name + postal code to narrow down the search results and ensure we get that specific restaurant back
    params = {'q':resto['lic_search_name']+' '+resto['lic_postal']}
    
    #pass a PC-like user-agent to trick google into giving us all the info we want
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    
    #pull the page and parse it with our HTMLParser (ParseRating)
    r = requests.get('https://www.google.ca/search',params=params,headers=headers)
    parser = ParseRating()
    parser.feed(r.text)
    rating = parser.data
    
    menulink = "https://www.toronto.ca/explore-enjoy/festivals-events/summerlicious/summerlicious-restaurants-menus/?view=tabList&dpa=yes&key=" + resto['lic_documentID']

    #write the rating to the CSV with some other details about the restaurant
    line = [resto['lic_restName'],rating,resto['lic_address'],resto['lic_postal'],resto['lic_lat'],resto['lic_lng'],resto['lic_lunchprice'],resto['lic_dinnerprice'],menulink]
    csvfile.writerow(line)
    
    #output status message and delay to avoid triggering flood protection on the server
    delay = random.randint(31,62)
    print "Just completed #" + str(count) + " of " + str(len(data["restaurants"])) + ": " + resto['lic_restName'] + " (rating: " + str(rating) + ") " + ("and resting for " + str(delay) +"sec" if count < len(data["restaurants"]) else "")
    if (count < len(data["restaurants"])):
      time.sleep(delay)