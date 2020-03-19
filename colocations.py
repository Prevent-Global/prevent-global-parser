class visit:

    def __init__(self, times, coordinates, address = None):
        self.times = times
        self.coordinates = coordinates
        self.address = address


class timeline:

    def __init__(self):
        self.intervals = []

    def add_interval(self, interval):
        self.intervals.append(interval)

    def merge(self, t):
        self.intervals = [*self.intervals, *t.intervals]

    def compute_overlap_with_interval(self, a):
        overlap = timeline()
        for b in self.intervals:
            c = (max(a[0], b[0]), min(a[1], b[1]))
            if c[0]!=c[1]:
                overlap.add_interval(c)
        return overlap


class colocation:

    def __init__(self, coordinates, address, timeline):
        colocation.coordinates = coordinates
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


class heatmap:

    def __init__(self):
#         ofc we need some database here, not a dictionary
        self.places = {}

    def add_visit(self, v):
        #adds visit of COVID case to the database
        if v.address not in self.places.keys():
            self.places[v.address] = timeline()

        self.places[v.address].add_interval(v.times)

    def compare_visit(self, v):
        if v.address in self.places.keys():
            overlap = self.places[v.address].compute_overlap_with_interval(v.times)
            return colocation(v.coordinates, v.address, overlap)

    def compare_person(self, p):
        co = extracted_colocations()
        for v in p.visits:
            c = self.compare_visit(v)
            if c!= None:
                if c.address in co.colocations.keys():
                    co.colocations[c.address].merge(c)
                else:
                    co.colocations[c.address] = c
        return co


class person:

    def __init__(self, age = None):
        self.age = age
        self.visits = []
        self.transits = []

    def add_visit(self, visit):
        self.visits.append(visit)

def extract_overlap(person, heatmap):
#     Computes the timeline of colocation of person with all people used to create the heatmap
#     Makes sense only for person not used to create the heatmap!
    total_overlap = timeline()
    for visit in person.visits:
        total_overlap.add_period(heatmap.check_visit(visit))
    return overlap
