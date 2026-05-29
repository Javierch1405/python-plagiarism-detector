class Dataset:
    def __init__(self, values):
        self.values = list(values)

    def average(self):
        accumulator = 0.0
        for v in self.values:
            accumulator = accumulator + v
        return accumulator / len(self.values)

    def variance(self):
        avg = self.average()
        squared = [(v - avg) ** 2 for v in self.values]
        return sum(squared) / len(self.values)

def run():
    sample = [4, 8, 15, 16, 23, 42]
    ds = Dataset(sample)
    print("mean:", ds.average())
    print("variance:", ds.variance())

run()
