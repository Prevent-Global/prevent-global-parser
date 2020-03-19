from parse import parse_file
from colocations import heatmap, person
import googlemaps
import os


API_key = os.environ.get('API_key')

gmaps = googlemaps.Client(key = API_key)

folder = 'sample_files/'
filenames = os.listdir(folder)

h = heatmap()
p = person()

for filename in filenames:
    visits = parse_file(folder+filename)
    p.add_visits(visits)
    h.add_visits(visits)

h1 = heatmap()
p1 = person()

for filename in filenames[:3]:
    visits = parse_file(folder+filename)
    p1.add_visits(visits)
    h1.add_visits(visits)

c = h.compare_person(p1)

for key in c.colocations:
    print(c.colocations[key].address, c.colocations[key].timeline.intervals[0])
