import db
from parse import parse_file

class visit:

    def __init__(self, times, place_id, address = None):
        self.times = times
        self.place_id = place_id
        self.address = address


class timeline:

    def __init__(self, intervals=[]):
        self.intervals = intervals

    def add_intervals(self, intervals):
        self.intervals.extend(intervals)

    def merge(self, t):
        self.intervals = [*self.intervals, *t.intervals]

    def compute_overlap_with_interval(self, a):
        overlap = timeline()
        for b in self.intervals:
            c = (max(a[0], b[0]), min(a[1], b[1]))
            if c[0]!=c[1]:
                overlap.add_intervals([c])
        return overlap


class colocation:

    def __init__(self, place_id, address, timeline):
        colocation.place_id = place_id
        colocation.address = address
        colocation.timeline = timeline

    def merge(self, c):
        assert self.address == c.address
        self.timeline.merge(c.timeline)


class extracted_colocations:

    def __init__(self):
        self.colocations = {}

    def add_colocation(self, c):
    #Note: somewhat redundant info in keys
        if c.address in self.colocations.keys():
            self.colocations[c.address].merge(c)
        else:
            self.colocations[c.address] = c

def compare_visit(conn, visit):
    if db.contains_place(conn, visit.place_id):
        intervals = [visit[1:] for visit in db.select_visits_by_place(conn, visit.place_id)]
        t = timeline(intervals)
        overlap = t.compute_overlap_with_interval(visit.times)
        return colocation(visit.place_id, visit.address, overlap)

    return None


def find_colocations(subject):
    with db.create_connection() as conn:
        co = extracted_colocations()
        for visit in subject.visits:
            c = compare_visit(conn, visit)
            if c is not None:
                if c.address in co.colocations:
                    co.colocations[c.address].merge(c)
                else:
                    co.colocations[c.address] = c

        return co

    return None


class heatmap:

    def __init__(self):
#         ofc we need some database here, not a dictionary
        self.places = {}

    def add_visit(self, v):
        #adds visit of COVID case to the database
        if v.address not in self.places.keys():
            self.places[v.address] = timeline()

        self.places[v.address].add_interval(v.times)

    def add_visits(self, visits):
            for v in visits:
                self.add_visit(v)

    def compare_visit(self, v):
        if v.address in self.places.keys():
            overlap = self.places[v.address].compute_overlap_with_interval(v.times)
            return colocation(v.place_id, v.address, overlap)

    def compare_subject(self, p):
        co = extracted_colocations()
        for v in p.visits:
            c = self.compare_visit(v)
            if c!= None:
                if c.address in co.colocations.keys():
                    co.colocations[c.address].merge(c)
                else:
                    co.colocations[c.address] = c
        return co


class subject:

    def __init__(self, history, age = None):
        self.age = age
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
                        self.visits.append(visit(v[1], place_id, v[2]))


def extract_overlap(subject, heatmap):
#     Computes the timeline of colocation of subject with all people used to create the heatmap
#     Makes sense only for subject not used to create the heatmap!
    total_overlap = timeline()
    for visit in subject.visits:
        total_overlap.add_period(heatmap.check_visit(visit))
    return overlap
