import numpy as np
from googleplaces import GooglePlaces, types, lang 
import xml.etree.cElementTree as ET
from glob import glob
import os
from parse import load_KML

API_key = os.environ.get('API_key')

google_places = GooglePlaces(API_key) 

def list_places_in_radius(center, radius):
    query_result = google_places.nearby_search( 
            lat_lng ={'lat': center[0], 'lng': center[1]}, 
            radius = radius, 
            types =[types.TYPE_BAR])
    bars = []
    for place in query_result.places:
        bars.append("%.7f" % place.geo_location['lng'] + ',' + "%.7f" % place.geo_location['lat'])
    
    query_result = google_places.nearby_search( 
            lat_lng ={'lat': center[0], 'lng': center[1]}, 
            radius = radius, 
            types =[types.TYPE_CAFE])
    cafes = []
    for place in query_result.places:
        bars.append("%.7f" % place.geo_location['lng'] + ',' + "%.7f" % place.geo_location['lat'])
    
    query_result = google_places.nearby_search( 
            lat_lng ={'lat': center[0], 'lng': center[1]}, 
            radius = radius, 
            types =[types.TYPE_HOSPITAL])
    hospitals = []
    for place in query_result.places:
        bars.append("%.7f" % place.geo_location['lng'] + ',' + "%.7f" % place.geo_location['lat'])
    
    return bars+cafes+hospitals

def generate_time_interval(day, max_len = 2):
    date = '2020-03-'+str(day).zfill(2)
    h, m, s = np.random.randint(0,24-max_len), np.random.randint(0,60), np.random.randint(0,60)
    start = str(h).zfill(2)+':'+str(m).zfill(2)+':'+str(s).zfill(2)
    hd, md, sd = np.random.randint(1,max_len), np.random.randint(0,60), np.random.randint(0,60)
    end = str(h+hd).zfill(2)+':'+str(md).zfill(2)+':'+str(sd).zfill(2)
    
    time = '  from '+ date + 'T' + start + '.111Z to ' + date + 'T' + end + '.111Z. Distance 0m'
    return time

def generate_file(day, coords_list, base_file_path, output_path):
    doc = load_KML(base_file_path)
    for child in doc[0]:
        if child.tag.split('}')[1] == 'Placemark':
            interval = generate_time_interval(day, max_len = 2)
            child[3].text = interval
            coords = np.random.choice(coords_list)
            child[4][0].text = coords

    tree = ET.ElementTree(doc)
    tree.write(output_path)

def generate_subject(subject_id, coords_list, directory):
    base_files = glob('base_files/*kml')
    os.mkdir(directory+'/'+str(subject_id))
    for day in range(8,23):
        base = np.random.choice(base_files)
        generate_file(day, coords_list, base, directory+'/'+str(subject_id)+'/history-2020-03-'+str(day)+'.kml')
    s_data = {'age': np.random.randint(18,80), 
              'weight' : np.random.randint(40,90),
              "country": "Poland",
                "tested": True,
                "testedPositive": bool(np.random.randint(3)==1),
                "assessmentResult": np.random.randint(10)
             }
    with open(directory + '/' + str(subject_id) + '/' + 'subject_info.json', 'w') as fp:
        json.dump(s_data, fp)

def generate_data(n_subjects, radius, directory):
    os.mkdir(directory)
    '''Generate 2 weeks of location history for n_subjects under 'directory'.
    The visited places will be in 'radius' from the Krakow city center    
    '''
    coords_list = list_places_in_radius((50.0698789, 19.9463714), radius)
    for i_sub in range(n_subjects):
        subject_id = np.random.randint(10**9)
        generate_subject(subject_id, coords_list, directory)
