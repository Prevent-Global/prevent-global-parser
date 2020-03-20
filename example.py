from parse import parse_file_add_to_db, parse_file
import os
from glob import glob

from colocations import subject, find_colocations
import db

def build_db():
    os.remove('prevent.db')
    db.setup()

    for fn in glob('sample_files/*kml'):
        parse_file_add_to_db(fn)

build_db()

subject_history = glob('sample_files/*kml')[3:]
s = subject(subject_history)

c = find_colocations(s)

for key in c.colocations:
    print(c.colocations[key].address, c.colocations[key].timeline.intervals[0])
