import json
from joblib import Parallel, delayed
from multiprocessing import cpu_count
from glob import glob
from pykml import parser
from lxml import etree
from datetime import datetime, timedelta
import googlemaps
import os

import db

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
    lon = float(node[4][0].text.split(',')[0])
    lat = float(node[4][0].text.split(',')[1])
    return (lat, lon)


def get_place(coordinates):
    # Need to be reverted for the purpose of googlemaps API compatibility
    # (BTW: wtf? It's exported from other Google service...)
    coords = coordinates[1], coordinates[0]
    return(gmaps.reverse_geocode(coords)[0]['formatted_address'])


def parse_file(filename):
    ''' parse a kml file and return a list of visits '''
    visits  = []
    doc = load_KML(filename)[0]
    for child in doc:
        if child.tag.split('}')[1] == 'Placemark' and child[3].text.startswith('  '):
        # Searching for double space is a dirty trick, bt there is no keyword like 'visit' or 'stay;
        # We need to check whether it work on files exported for other people as well
            visits.append((get_coordinates(child), get_times(child)))

    addresses = Parallel(n_jobs=cpu_count())(delayed(get_place)(v[0]) for v in visits)
    for i, address in enumerate(addresses):
        visits[i] += (address,)

    return visits

def parse_file_add_to_db(filename, subject_id, info):
    conn = db.create_connection()
    if not db.contains_subject(conn, subject_id):
        db.add_subject(conn, (subject_id, info['age'], info['weight'], info['country'], info['tested'], info['testedPositive'], info['assessmentResult']))


    visits = parse_file(filename)
    for v in visits:
        place = (int(v[0][0]*1e7), int(v[0][1]*1e7), v[2])
        place_id = db.find_place_id(conn, place)
        if place_id is None:
            place_id = db.add_place(conn, place)
        beg = v[1][0]
        end = v[1][1]
        db.add_visit(conn, (place_id, subject_id, beg, end))

    conn.commit()

def parse_subject_dir(path):
    subject_ID = int(path.split('/')[-1])
    with open(path+'/subject_info.json', 'r') as f:
        info = json.load(f)

    for fn in glob(path + "/*kml"):
        parse_file_add_to_db(fn, subject_ID, info)
