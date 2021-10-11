class Interval:

    def __init__(self, lb, ub):
        self.lb = lb
        self.ub = ub

    def intersection(self, interval):
        if isinstance(interval, Interval):
            return Interval(max(self.lb, interval.lb), min(self.ub, interval.ub))
        raise ValueError()

    def is_empty(self):
        return self.lb > self.ub

    def __contains__(self, item):
        return self.lb <= item <= self.ub

    def __str__(self):
        return f"[{self.lb}, {self.ub}]"

    def __repr__(self):
        return f"Interval({self.lb}, {self.ub})"
