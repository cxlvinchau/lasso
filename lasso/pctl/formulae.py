class StateFormula:

    def __init__(self,dtmc):
        """Super class for state formulae"""
        # States that satisfy this formula
        self.all = set(dtmc.states)
        self.states = set()
        self.dtmc = dtmc

    def eval(self):
        """Needs to be overridden in child class and call eval on children"""
        pass

    def __and__(self, other):
        if isinstance(other,StateFormula):
            return Conjunction(self,other,self.dtmc)

    def __or__(self, other):
        if isinstance(other,StateFormula):
            return Disjunction(self,other,self.dtmc)

    def __neg__(self):
        return Negation(self,self.dtmc)

    def __str__(self):
        pass


class Atomic(StateFormula):

    def __init__(self,label,dtmc):
        super().__init__(dtmc)
        self.label = label

    def add_states(self,*args):
        for s in args:
            self.states.add(s)

    def __str__(self):
        return self.label


class Conjunction(StateFormula):
    """Conjunction state formula"""
    def __init__(self,f1,f2,dtmc):
        super().__init__(dtmc)
        self.f1 = f1
        self.f2 = f2

    def eval(self):
        self.f1.eval()
        self.f2.eval()
        self.states = self.f1.states.intersection(self.f2.states)


class Disjunction(StateFormula):
    """Disjunction state formula"""
    def __init__(self,f1,f2,dtmc):
        super().__init__(dtmc)
        self.f1 = f1
        self.f2 = f2

    def eval(self):
        self.f1.eval()
        self.f2.eval()
        self.states = self.f1.states.union(self.f2.states)


class Negation(StateFormula):
    """Negation state formula"""
    def __init__(self,f,dtmc):
        super().__init__(dtmc)
        self.f = f

    def eval(self):
        self.f.eval()
        self.states = self.dtmc.states - self.f.states

