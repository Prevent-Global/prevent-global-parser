import db
from parse import parse_file

class visit:

    def __init__(self, subject_id, times, place_id, address = None):
        self.subject_id = subject_id
        self.times = times
        self.place_id = place_id
        self.address = address

def compute_overlap(a, b):
    c = (max(a[0], b[0]), min(a[1], b[1]))
    if c[0]!=c[1]:
        return c
    return None

class colocation:

    def __init__(self, infected_id, subject_id, place_id, address, times):
        self.infected_id = infected_id
        self.subject_id = subject_id
        self.place_id = place_id
        self.address = address
        self.times = times

def compare_visit(conn, visit):
    colocations = []
    if db.contains_place(conn, visit.place_id):
        visits = db.select_visits_by_place(conn, visit.place_id)
        for v in visits:
            infected_id = v[2]
            infected_visit_times = v[3], v[4]
            overlap = compute_overlap(infected_visit_times, visit.times)
            if overlap is not None:
                colocations.append(colocation(infected_id, visit.subject_id, visit.place_id, visit.address, overlap))

    return colocations

def find_colocations(subject):
    with db.create_connection() as conn:
        colocations = []
        for visit in subject.visits:
            colocations.extend(compare_visit(conn, visit))

        return colocations

class subject:

    def __init__(self, history, subject_id, info):
        self.subject_id = subject_id
        self.info = info
        self.visits = []
        self.transits = []

        with db.create_connection() as conn:
            for fn in history:
                visits = parse_file(fn)
                for v in visits:
                    latE7 = int(v[0][0]*1e7)
                    lonE7 = int(v[0][1]*1e7)
                    place_id = db.find_place_id(conn, (latE7, lonE7, v[2]))
                    if place_id is not None:
                        self.visits.append(visit(subject_id, v[1], place_id, v[2]))
