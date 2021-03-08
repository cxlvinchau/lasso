from graphviz import Digraph

from directed_graph import DirectedGraph

from lasso_constants import Comparator


class TimedAutomaton:

    def __init__(self):
        self.states = set()
        self.initial = None
        self.actions = set()
        self.transitions = set()
        self.clocks = set()
        self.clock_to_max = dict()
        self.id = -1
        self.initial_location = None

    def add_location(self, name):
        self.id += 1
        l = Location(name, id=id)
        if self.id == 0:
            self.initial_location = l
        self.states.add(l)
        return l

    def add_transition(self, source, action, target, reset=set(), guard=None):
        self.clocks = self.clocks.union(reset)
        self.actions.add(action)
        if guard is not None:
            self.clocks.add(guard.clock)
            if guard.clock not in self.clock_to_max:
                self.clock_to_max[guard.clock] = 0
            self.clock_to_max[guard.clock] = max(self.clock_to_max[guard.clock], guard.value)
        t = Transition(source, action, target, reset=reset, guard=guard)
        self.transitions.add(t)
        return t

    def to_dotty(self, file="out"):
        print(self.clock_to_max)
        dot = Digraph()
        for s in self.states:
            dot.node(s.name)
        for t in self.transitions:
            dot.edge(t.source.name, t.target.name,
                     label="{}, {}, {}".format(t.action, "True" if t.guard is None else t.guard,
                                                 t.reset if t.reset else ""))
        dot.render(file, view=True)

    def get_transitions(self, location):
        return [t for t in self.transitions if t.source == location]

    def generate(self):
        dot = Digraph()
        if self.initial_location is None:
            return
        init = Region(self.initial_location,[ClockRegion(c, 0, 0) for c in self.clocks])
        worklist = [init]
        visited = set()

        # For plotting
        edges = []
        dg = DirectedGraph()

        while worklist:
            region = worklist.pop()
            print(region)
            dg.add_vertex(region.to_node())
            # Add to visited set
            visited.add(region)
            transitions = self.get_transitions(region.location)

            # Generate discrete transitions
            for t in transitions:
                guard = t.guard
                # Check if discrete transition is enabled
                if guard is None or all([guard.is_satisfied_by(cl) for cl in region.clock_regions]):
                    succ = Region(t.target,region.clock_regions).reset_clocks(t.reset)
                    if succ not in visited:
                        worklist.append(succ)
                    edges.append((region.to_node(),succ.to_node()))
            # Generate delay transitions
            succ_region = [cl.get_successor(self.clock_to_max[cl.clock]) for cl in region.clock_regions]
            succ = Region(region.location,succ_region)
            if succ not in visited:
                worklist.append(succ)
            edges.append((region.to_node(),succ.to_node()))

        for s, t in edges:
            dg.add_edge(s, t)

        dg.to_dotty()
        print(len(dg.vertices))


class Location:

    def __init__(self, name, id=None,invariants=[]):
        self.name = name
        self.id = id
        self.invariants = []

    def __eq__(self, other):
        if isinstance(other, Location):
            return other.name == self.name and self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id) * hash(self.name)

    def __str__(self):
        return self.name


class Transition:

    def __init__(self, source, action, target, reset=set(), guard=None):
        self.source = source
        self.action = action
        self.reset = reset
        self.guard = guard
        self.target = target

    def __eq__(self, other):
        if isinstance(other, Transition):
            return self.source == other.source and self.target == other.target and self.action == other.action
        return False

    def __hash__(self):
        return hash(self.source) * hash(self.target) * hash(self.action)


class Constraint:

    def __init__(self, clock, comparator, value):
        self.clock = clock
        self.comparator = comparator
        self.value = value

    def is_satisfied_by(self, clock_region):
        if clock_region.clock != self.clock:
            return True
        # Handle equals comparator
        if self.comparator == Comparator.EQUALS:
            if clock_region.is_singleton() and clock_region.lower == self.value:
                return True
        # handle < and <=
        elif self.comparator == Comparator.SMALLER or self.comparator == Comparator.SMALLER_EQUALS:
            if clock_region.upper < self.value:
                return True
            if clock_region.is_open() and clock_region.upper == self.value:
                return True
            return self.comparator == Comparator.SMALLER_EQUALS and clock_region.upper == self.value
        # handle > and >=
        elif self.comparator == Comparator.GREATER or self.comparator == Comparator.GREATER_EQUALS:
            if clock_region.lower > self.value:
                return True
            if clock_region.is_open() and clock_region.lower == self.value:
                return True
            return self.comparator == Comparator.GREATER_EQUALS and clock_region.lower == self.value
        return False

    def __str__(self):
        return "{} {} {}".format(self.clock, self.comparator.value, self.value)


class ClockRegion:

    def __init__(self, clock, lower, upper, open=True):
        self.clock = clock
        self.lower = lower
        self.upper = upper
        self.open = open if lower != upper else False

    def is_singleton(self):
        return self.lower == self.upper

    def is_open(self):
        return self.open

    def get_successor(self,max_val):
        if self.lower >= max_val and self.is_open():
            return self
        if self.open:
            return ClockRegion(self.clock, self.upper, self.upper)
        else:
            return ClockRegion(self.clock, self.upper, self.upper + 1)

    def __str__(self):
        if self.lower == self.upper:
            return "{0} : {{{1}}}".format(self.clock, self.upper)
        else:
            return "{} : ({},{})".format(self.clock, self.lower, self.upper)

    def __eq__(self, other):
        if isinstance(other, ClockRegion):
            return self.clock == other.clock and self.lower == other.lower and self.upper == other.upper and self.open == other.open
        return False

    def __hash__(self):
        return hash(self.clock) * hash(self.upper) * hash(self.lower)

    def __copy__(self):
        copy = ClockRegion(self.clock,self.lower,self.upper,open=self.open)
        return copy

    def reset(self):
        self.lower = 0
        self.upper = 0
        self.open = False


class Region:

    def __init__(self, location, clock_regions=[]):
        self.location = location
        self.clock_regions = clock_regions

    def satisfies(self, constraint):
        return all([constraint.is_satisfied_by(cl) for cl in self.clock_regions])

    def reset_single_clock(self,clock):
        new_region = self.__copy__()
        clock_region = None
        for cl in new_region.clock_regions:
            if cl.clock == clock:
                clock_region = cl
                break
        if clock_region is not None:
            clock_region.reset()
        return new_region

    def reset_clocks(self,clocks):
        region = self.__copy__()
        for c in clocks:
            region = self.reset_single_clock(c)
        return region

    def __copy__(self):
        clock_regions = [cl.__copy__() for cl in self.clock_regions]
        return Region(self.location,clock_regions)

    def to_node(self):
        return self.location.name + "\n" + ", ".join([str(cl) for cl in self.clock_regions])

    def __str__(self):
        return self.to_node()

    def __eq__(self, other):
        if isinstance(other,Region):
            return other.location == self.location and other.clock_regions == self.clock_regions

    def __hash__(self):
        return hash(self.location)*sum(hash(cl) for cl in self.clock_regions)


def example1():
    ta = TimedAutomaton()
    # Add states
    l0 = ta.add_location("on")
    l1 = ta.add_location("off")
    # Add transitions
    constr = Constraint("x", Comparator.SMALLER_EQUALS, 1)
    ta.add_transition(l0, "a", l1, guard=constr,reset=["x"])
    ta.generate()
    # Visualize
    #ta.to_dotty()


def example2():
    ta = TimedAutomaton()
    # Add locations
    s1 = ta.add_location("s1")
    s2 = ta.add_location("s2")
    s3 = ta.add_location("s3")
    # Add transitions
    ta.add_transition(s1,"c",s3,guard=Constraint("y",Comparator.GREATER,1))
    ta.add_transition(s1,"a",s2,reset=["x"])
    ta.add_transition(s2,"b",s1,guard=Constraint("x",Comparator.SMALLER_EQUALS,1))
    ta.generate()


def example3():
    ta = TimedAutomaton()
    s0 = ta.add_location("s0")
    s1 = ta.add_location("s1")
    s2 = ta.add_location("s2")
    ta.add_transition(s0,"a",s1,guard=Constraint("x",Comparator.GREATER,2))
    ta.add_transition(s1,"a",s2)
    ta.generate()


if __name__ == "__main__":
    example3()
