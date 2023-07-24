import csv
import pandas as pd

class Dataset:

    def __init__(self, file):
        with open(file, mode='r') as f:
            reader = csv.DictReader(f)
            d = []
            for row in reader:
                d.append(row)
            df = pd.DataFrame(d)
            self.vars = list(df.columns)
            self.dataset = df.to_dict('records')
            self.memoize = {}
            self.domains = {}
            self.uniques = []
            self.counts = {}
            self.space_size = 1
            for o in self.dataset:
                if o not in self.uniques:
                    self.uniques.append(o)
                self.counts[repr(o)] = self.counts.get(repr(o),0) + 1
            for v in self.vars:
                self.domains[v] = set([])
                for i in self.dataset:
                    self.domains[v].add(i[v])
                self.domains[v] = list(self.domains[v])
                self.space_size *= len(self.domains[v])

