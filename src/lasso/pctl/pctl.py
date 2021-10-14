from lasso.models.dtmc import DTMC, State

import abc
import numpy as np

from lasso.utils import Interval


class StateFormula(abc.ABC):
    """Super class for all state formulae"""

    def __init__(self):
        self.states = None

    @abc.abstractmethod
    def eval(self, dtmc: DTMC) -> set:
        pass


class PathFormula(abc.ABC):
    """Super class for all path formulae"""

    def __init__(self):
        pass

    @abc.abstractmethod
    def compute_probability(self, state: State, dtmc: DTMC):
        pass


class TT(StateFormula):
    """Corresponds to true"""

    def __init__(self):
        super().__init__()

    def __eq__(self, other):
        if isinstance(other, TT):
            return True
        return False

    def __hash__(self):
        return hash(True)

    def eval(self, dtmc: DTMC):
        self.states = dtmc.states
        return self.states

    def __repr__(self):
        return f"TT()"

    def __str__(self):
        return "true"


class FF(StateFormula):
    """Corresponds to true"""

    def __init__(self):
        super().__init__()

    def __eq__(self, other):
        if isinstance(other, FF):
            return True
        return False

    def __hash__(self):
        return hash(False)

    def eval(self, dtmc: DTMC):
        self.states = set()
        return self.states

    def __repr__(self):
        return f"FF()"

    def __str__(self):
        return "false"


class AP(StateFormula):
    """Atomic proposition"""

    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol

    def __eq__(self, other):
        if isinstance(other, AP):
            return other.symbol == self.symbol
        return False

    def __hash__(self):
        return hash(self.symbol)

    def eval(self, dtmc: DTMC):
        if self.states is None:
            self.states = set([state for state in dtmc.states if self in state.ap])
        return self.states

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return f"AP({self.symbol})"


class Conjunction(StateFormula):
    """Conjunction of two state formulae"""

    def __init__(self, phi1: StateFormula, phi2: StateFormula):
        super().__init__()
        if not isinstance(phi1, StateFormula) or not isinstance(phi2, StateFormula):
            raise ValueError("Passed formulae have to be state formulae")
        self.phi1 = phi1
        self.phi2 = phi2

    def eval(self, dtmc: DTMC):
        if self.states is None:
            self.states = self.phi1.eval(dtmc).intersection(self.phi2.eval(dtmc))
        return self.states

    def __str__(self):
        return f"({str(self.phi1)} & {str(self.phi2)})"


class Disjunction(StateFormula):
    """Disjunction of two state formulae"""

    def __init__(self, phi1: StateFormula, phi2: StateFormula):
        super().__init__()
        if not isinstance(phi1, StateFormula) or not isinstance(phi2, StateFormula):
            raise ValueError("Passed formulae have to be state formulae")
        self.phi1 = phi1
        self.phi2 = phi2

    def eval(self, dtmc: DTMC):
        if self.states is None:
            self.states = self.phi1.eval(dtmc).union(self.phi2.eval(dtmc))
        return self.states

    def __str__(self):
        return f"({str(self.phi1)} | {str(self.phi2)})"


class Negation(StateFormula):
    """Negation of two state formulae"""

    def __init__(self, phi: StateFormula):
        super().__init__()
        if not isinstance(phi, StateFormula):
            raise ValueError("Passed formula has to be state formula")
        self.phi = phi

    def eval(self, dtmc: DTMC):
        if self.states is None:
            self.states = dtmc.states.difference(self.phi.eval(dtmc))
        return self.states

    def __str__(self):
        return f"!{str(self.phi)}"


class P(StateFormula):
    """Probability state formula"""

    def __init__(self, interval: Interval, psi: PathFormula):
        super().__init__()
        if not isinstance(psi, PathFormula):
            raise ValueError("Passed formula has to be path formula")
        self.interval = interval
        self.psi = psi

    def eval(self, dtmc: DTMC) -> set:
        if self.states is None:
            self.states = set([s for s in dtmc.states if self.psi.compute_probability(s, dtmc) in self.interval])
        return self.states

    def __str__(self):
        return f"P{str(self.interval)}({str(self.psi)})"


class Next(PathFormula):
    """Next path formula"""

    def __init__(self, phi: StateFormula):
        super().__init__()
        if not isinstance(phi, StateFormula):
            raise ValueError("Passed formula has to be state formula")
        self.phi = phi

    def compute_probability(self, state: State, dtmc: DTMC):
        states = self.phi.eval(dtmc)
        distr = dtmc.transient(1, {state: 1.0})
        return np.sum(distr[[s.id for s in states]])

    def __str__(self):
        return f"(X {str(self.phi)})"


class BoundedUntil(PathFormula):
    """Bounded until formula"""

    def __init__(self, phi1: StateFormula, phi2: StateFormula, steps: int):
        super().__init__()
        if not isinstance(phi1, StateFormula) or not isinstance(phi2, StateFormula):
            raise ValueError("Passed formulae have to be state formulae")
        self.phi1 = phi1
        self.phi2 = phi2
        if not isinstance(steps, int) or steps < 0:
            raise ValueError("Steps has to be a non-negative integer")
        self.steps = steps

    def compute_probability(self, state: State, dtmc: DTMC):
        states1 = self.phi1.eval(dtmc)
        states2 = self.phi2.eval(dtmc)
        res = dtmc.compute_reachability(states2, bad_states=dtmc.states - states1, steps=self.steps)
        return res[state.id]

    def __str__(self):
        return f"{str(self.phi1)} U<={self.steps} {str(self.phi2)}"


class Until(PathFormula):

    def __init__(self, phi1: StateFormula, phi2: StateFormula):
        super().__init__()
        if not isinstance(phi1, StateFormula) or not isinstance(phi2, StateFormula):
            raise ValueError("Passed formulae have to be state formulae")
        self.phi1 = phi1
        self.phi2 = phi2

    def compute_probability(self, state: State, dtmc: DTMC):
        states1 = self.phi1.eval(dtmc)
        states2 = self.phi2.eval(dtmc)
        res = dtmc.compute_reachability(states2, bad_states=dtmc.states - states1)
        print(res)
        return res[state.id]

    def __str__(self):
        return f"{str(self.phi1)} U {str(self.phi2)}"