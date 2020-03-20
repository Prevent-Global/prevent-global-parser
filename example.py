import json
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
with open('sample_files/2/subject_info.json', 'r') as f:
    info = json.load(f)

s = subject(subject_history, '2', info)

colocations = find_colocations(s)

with db.create_connection() as conn:
    for c in colocations:
        print(c.infected_id, c.subject_id, c.address, c.times)
        db.add_colocation(conn, (c.infected_id, c.subject_id, c.place_id, *c.times))
