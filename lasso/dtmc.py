import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import math

class DTMC:
    """Represents finite discrete time-homogeneous markov chain"""

    def __init__(self):
        self.states = set()
        self.transitions = set()
        self.state_id = 0
        self.transition_id = 0
        self.transition_matrix = None
        self.initial_state = None

    def add_state(self, label):
        """Adds state to DTMC and returns it"""
        s = State(label, id=self.state_id)
        if self.initial_state is None:
            self.initial_state = s
        self.state_id += 1
        self.states.add(s)
        return s

    def add_transition(self, source, p, target):
        """Adds transition from source to target with probability p"""
        if p > 0:
            source.add_successor(p, target)
            self.transitions.add(Transition(source, p, target))

    def __repr__(self):
        return "DTMC()"

    def __str__(self):
        return "DTMC\nStates: {}\nTransition: {}".format(self.states, self.transitions)

    def visualize(self, seed=1):
        """Visualizes the DTMC"""
        seed = seed
        random.seed(seed)
        np.random.seed(seed)
        G = nx.DiGraph()
        G.add_nodes_from(self.states)
        G.add_edges_from([(t.source, t.target, {"p": t.p}) for t in self.transitions])
        pos = nx.spring_layout(G, seed=1)
        nx.draw(G, with_labels=True, font_weight='bold')
        edge_labels = nx.get_edge_attributes(G, 'p')
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
        plt.show()

    def compute_transition_matrix(self) -> None:
        """Computes the transition matrix for the DTMC"""
        self.transition_matrix = np.zeros((len(self.states), len(self.states)))
        for s in self.states:
            for p, successor in s.get_successors():
                self.transition_matrix[s.id, successor.id] = p

    def transient(self,t):
        """Computes the transient distribution at time step t"""
        if self.transition_matrix is None:
            self.compute_transition_matrix()
        pi = np.zeros(len(self.states))
        pi[self.initial_state.id] = 1
        return pi.dot(np.linalg.matrix_power(self.transition_matrix, t))

    def is_irreducible(self):
        """Check if chain is irreducible"""
        matrix = np.full((len(self.states),len(self.states)),False)
        row, col = np.diag_indices(matrix.shape[0])
        matrix[row,col] = np.full(len(self.states),True)
        for t in self.transitions:
            matrix[t.source.id,t.target.id] = True
        for s1 in self.states:
            for s2 in self.states:
                for k in self.states:
                    if not matrix[s1.id,s2.id]:
                        matrix[s1.id,s2.id] = matrix[s1.id,k.id] and matrix[k.id,s2.id]
        return matrix.all()

    def __is_aperiodic(self):
        """Check if a chain is aperiodic. Assumes chain is irreducible"""
        marked = set()
        level = dict()
        period = {"value" : 0}

        def aux(s, l):
            _, successors = zip(*s.get_successors())
            if period["value"] == 1:
                return
            if s not in marked:
                marked.add(s)
                level[s] = l
                for _, succ in s.get_successors():
                    aux(succ, l + 1)
            else:
                period["value"] = math.gcd(period["value"],l-level[s])
        aux(self.initial_state,0)
        return period["value"] == 1

    def is_ergodic(self):
        """Check if chain is ergodic"""
        return self.is_irreducible() and self.__is_aperiodic()



class State:
    """State in Markov chain"""

    def __init__(self, label, id=0):
        self.label = label
        self.successors = set()
        self.id = id

    def add_successor(self, p, state):
        self.successors.add(Transition(self, p, state))

    def get_successors(self):
        return [(t.p, t.target) for t in self.successors]

    def __eq__(self, other):
        if isinstance(other, State):
            return self.label == other.label
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.id

    def __repr__(self):
        return "State({},id={})".format(self.label, self.id)

    def __str__(self):
        return "s{}".format(self.id)


class Transition:
    """Transition in Markov chain"""

    def __init__(self, source, p, target):
        self.source = source
        self.p = p
        self.target = target
        self.id = id

    def __eq__(self, other):
        if isinstance(other, Transition):
            return self.source == other.source and self.target == other.target and self.p == other.p
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.source, self.p, self.target))

    def __repr__(self):
        return "Transition({},{},{})".format(self.source, self.p, self.target)

    def __str__(self):
        return "{} -{}-> {}".format(self.source, self.p, self.target)
