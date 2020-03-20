from parse import parse_subject_dir
import os
from glob import glob

from colocations import subject, find_colocations
import db

def build_db():
    os.remove('prevent.db')
    db.setup()

    parse_subject_dir('sample_files/1')

build_db()

subject_history = glob('sample_files/2/*kml')
s = subject(subject_history)

c = find_colocations(s)

for key in c.colocations:
    print(c.colocations[key].address, c.colocations[key].timeline.intervals[0])
