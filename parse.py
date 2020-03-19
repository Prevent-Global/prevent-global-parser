from pykml import parser
from lxml import etree
from datetime import datetime, timedelta
import googlemaps
import os

from colocations import visit
from db import create_connection, add_place, add_visit, find_place_id

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
    starting_time = int(datetime.strptime(temp, '%Y-%m-%dT%H:%M:%S').timestamp())

    temp = node[3].text.split(' to ')[1].split('.')[0]
    end_time = int(datetime.strptime(temp, '%Y-%m-%dT%H:%M:%S').timestamp())
    return(starting_time, end_time)


def get_coordinates(node):
    # TODO is it correct or should be the other way around?
    lat = float(node[4][0].text.split(',')[0])
    lon = float(node[4][0].text.split(',')[1])
    return (lat, lon)


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

    return visits

def parse_file_add_to_db(filename):
    conn = create_connection()
    visits = parse_file(filename)
    for v in visits:
        place = (v.coordinates[0]*1e7, v.coordinates[1]*1e7, v.address)
        place_id = find_place_id(conn, place)
        if place_id is None:
            place_id = add_place(conn, place)
        beg = v.times[0]
        end = v.times[1]
        add_visit(conn, (place_id, beg, end))

    conn.commit()
