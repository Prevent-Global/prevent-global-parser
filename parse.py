from pykml import parser
from lxml import etree
from datetime import datetime, timedelta
import googlemaps
import os

API_key = os.environ.get('API_key')

gmaps = googlemaps.Client(key = API_key)

def load_KML(filename):
    with open(filename) as f:
        doc = parser.parse(f)
#  if you know other way to 'unobjectify' this etree, do not hesitate!
    s = etree.tostring(doc.getroot())
    return etree.fromstring(s)


def get_times(node):
# input: 'Placemark' event
    temp = node[3].text.split('from ')[1].split('.')[0]
    starting_time = datetime.strptime(temp, '%Y-%m-%dT%H:%M:%S')

    temp = node[3].text.split(' to ')[1].split('.')[0]
    end_time = datetime.strptime(temp, '%Y-%m-%dT%H:%M:%S')
    return(starting_time, end_time)


def get_coordinates(node):
# Need to be reverted for the purpose of googlemaps API compatibility
# (BTW: wtf? It's exported from other Google service...)
    coordinates = node[4][0].text.split(',')[1]+','+node[4][0].text.split(',')[0]
    return(coordinates)


def get_place(node):
# Need to be reverted for the purpose of googlemaps API compatibility
# (BTW: wtf? It's exported from other Google service...)
    coordinates = node[4][0].text.split(',')[1]+','+node[4][0].text.split(',')[0]
    return(gmaps.reverse_geocode(coordinates)[0]['formatted_address'])


def parse_file(filename):
    ''' parse a kml file and return a list of visits '''
    visits  = []
    doc = load_KML(filename)[0]
    for child in doc:
        if child.tag.split('}')[1] == 'Placemark':
# Searching for double space is a dirty trick, bt there is no keyword like 'visit' or 'stay;
# We need to check whether it work on files exported for other people as well
            if child[3].text.startswith('  '):
                visits.append(visit(get_times(child), get_coordinates(child), get_place(child)))
