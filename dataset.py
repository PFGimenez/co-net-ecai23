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
            self.dataset_len = len(df)
            self.domains = {}
            self.counts = {}
            self.uniques = df.groupby(df.columns.tolist(), as_index=False).size().to_dict('records')
            for o in self.uniques:
                self.counts[repr(o)] = o.pop("size")
            for v in self.vars:
                self.domains[v] = df[v].unique()
