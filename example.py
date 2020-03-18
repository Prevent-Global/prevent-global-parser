from utils import heatmap, person, parse_file
import googlemaps
import os


API_key = os.environ.get('API_key')

gmaps = googlemaps.Client(key = API_key)

folder = 'sample_files/'
filenames = os.listdir(folder)

h = heatmap()
p = person()

for filename in filenames:
    parse_file(folder+filename, p, h)

h1 = heatmap()
p1 = person()


for filename in filenames[:3]:
    parse_file(folder+filename, p1, h1)

c = h.compare_person(p1)

for key in c.colocations:
    print(c.colocations[key].address, c.colocations[key].timeline.intervals[0])
