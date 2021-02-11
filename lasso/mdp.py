class MDP:

    def __init__(self):
        self.states = set()
        self.initial = None
        self.id = -1

    def set_initial_state(self,state):
        self.initial = state

    def add_state(self,name,**kwargs):
        self.id += 1
        s = State(name,id=self.id,**kwargs)
        self.states.add(s)
        return s


class State:

    def __init__(self,name,label=None,id=None):
        self.name = name
        self.label = label
        self.id = id
        self.action_to_succs = dict()

    def add_succ(self,succ,action=None,p=1):
        distr = self.action_to_succs.setdefault(action,dict())
        distr[succ] = p

    def __eq__(self, other):
        if isinstance(other, State):
            return self.label == other.label
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.id

    def __repr__(self):
        return "State({},label={},id={})".format(self.name,self.label, self.id)

    def __str__(self):
        return self.name


if __name__ == "__main__":
    mdp = MDP()
    s1 = mdp.add_state("s1",label="Test")
    print(repr(s1))

