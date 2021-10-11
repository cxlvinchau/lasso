from typing import Union

import numpy as np


class State:
    """State of a DTMC"""

    def __init__(self, id, name=None, ap=[]):
        self.id = id
        self.name = name if name else f"s{id}"
        self.ap = ap

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        if isinstance(other, State):
            return other.id == self.id
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"State({self.id}, name={self.name}, ap={self.ap})"


class Transition:
    """Transition of a DTMC"""

    def __init__(self, s1: State, s2: State, p: Union[float, int]):
        self.s1 = s1
        self.s2 = s2
        self.p = p

    def __hash__(self):
        return hash(self.s1) + hash(self.s2) - hash(self.p)

    def __eq__(self, other):
        if isinstance(other, Transition):
            return other.s1 == self.s1 and other.s2 == self.s2
        return False

    def __str__(self):
        return f"{self.s1} -- {self.p} --> {self.s2}"

    def __repr__(self):
        return f"Transition({self.s1, self.s2, self.p})"


class DTMC:
    """Discrete-Time Markov Chain implementation"""

    def __init__(self):
        self.states = set()
        self.transitions = set()
        self._counter = 0
        self.transition_matrix = None

    def add_state(self, name=None, ap=None):
        """
        Creates a new state and adds it to the DTMC. The newly created state is returned.

        :param name: Name of the state
        :param ap: Atomic propositions
        :return: State
        """
        if ap is None:
            ap = []
        s = State(self._counter, name=name, ap=ap)
        self._counter += 1
        self.states.add(s)
        return s

    def add_transition(self, s1: State, s2: State, p: [float, int]):
        """
        Creates a transition from s1 to s2 with probability p. Returns the created transition.

        :param s1: Source state of DTMC
        :param s2: Target state of DTMC
        :param p: Probability
        :return: Transition
        """
        t = Transition(s1, s2, p)
        self.transitions.add(t)
        return t

    def compute_transition_matrix(self):
        """
        Computes and updates the transition matrix

        :return: transition_matrix
        """
        self.transition_matrix = np.zeros((len(self.states), len(self.states)))
        for t in self.transitions:
            self.transition_matrix[t.s1.id][t.s2.id] = t.p
        return self.transition_matrix

    def transient(self, steps, init: [np.ndarray, dict]):
        """
        Computes the transient distribution for a given time step and initial distribution.

        :param steps: An integer corresponding to the time step
        :param init: Initial distribution, either an np.ndarray or dictionary that maps states to probabilities
        :return: Transient distribution
        """
        if isinstance(init, dict):
            init_dict = init
            init = np.zeros(len(self.states))
            for k, v in init_dict.items():
                init[k.id] = v
        self.compute_transition_matrix()
        transition_mat = np.linalg.matrix_power(self.transition_matrix, steps)
        return np.matmul(init, transition_mat)

    def compute_reachability(self, goal_states, bad_states=set(), steps=None):
        """
        Computes the reachability probability.

        :param goal_states: States that should be reached
        :param bad_states: States that need to be avoided
        :param steps: Step bound, if not given the bound is assumed to be infinite
        :return: Reachability probability
        """
        # Find states that can actually reach goal states
        good_states = set()
        size = -1
        while len(good_states) != size:
            size = len(good_states)
            for s in [s for s in self.states if s not in goal_states]:
                for t in self.transitions:
                    if s == t.s1 and t.s2 in goal_states:
                        good_states.add(s)
        bad_states = set([s for s in bad_states if s not in goal_states])
        good_states -= set(bad_states)
        good_states = list(good_states)
        bad_states = list(bad_states)
        goal_states = list(goal_states)
        self.compute_transition_matrix()
        if steps:
            # Bounded reachability
            x = np.zeros((len(good_states),1))
            P = self.transition_matrix
            A = P[[s.id for s in good_states], :][:, [s.id for s in good_states]]
            b = np.sum(P[[s.id for s in good_states], :][:, [s.id for s in goal_states]], axis=1)
            for i in range(steps):
                x = np.matmul(A, x) + b
            val = np.zeros(len(self.states))
            val[[s.id for s in goal_states]] = 1.0
            val[[s.id for s in bad_states]] = 0.0
            val[[s.id for s in good_states]] = x
            return val
        else:
            # Unbounded reachability
            pass
            # TODO
