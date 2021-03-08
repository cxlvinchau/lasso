from graphviz import Digraph

from lp_mean_payoff import LPMeanPayoff
from value_iteration import ValueIteration


class MDP:

    def __init__(self):
        self.states = set()
        self.initial = None
        self.actions = set()
        self.transitions = set()
        self.id = -1

    def set_initial_state(self, state):
        self.initial = state

    def add_state(self, name, **kwargs):
        self.id += 1
        s = State(name, id=self.id, **kwargs)
        self.states.add(s)
        return s

    def add_edge(self, source, target, action, p=1, reward=None):
        self.actions.add(action)
        source.add_succ(target, action, p=p, reward=reward)
        self.transitions.add(Transition(source, action, target, p=p, reward=reward))

    def to_dotty(self, file="out"):
        dot = Digraph()
        for s in self.states:
            dot.node(s.name)
        for t in self.transitions:
            dot.edge(t.source.name, t.target.name, label="{}, {}".format(t.action, t.p) + ("" if t.reward is None else ", r: " + str(t.reward)))
        dot.render(file, view=True)


class Transition:
    def __init__(self, source, action, target, p=1, reward=None):
        self.source = source
        self.action = action
        self.p = p
        self.target = target
        self.reward = reward

    def __eq__(self, other):
        if type(other) == Transition:
            return self.source == other.source and self.target == other.target and self.action == other.action
        return False

    def __hash__(self):
        return hash(self.source) * hash(self.target) * hash(self.action)


class State:

    def __init__(self, name, label=None, id=None):
        self.name = name
        self.label = label
        self.id = id
        self.action_to_succs = dict()
        self.action_to_reward = dict()
        self.enabled_actions = set()

    def add_succ(self, succ, action, p=1, reward=None):
        self.enabled_actions.add(action)
        distr = self.action_to_succs.setdefault(action, dict())
        distr[succ] = p
        if reward is not None:
            self.action_to_reward[action] = reward

    def get_reward(self, action):
        if action in self.action_to_reward:
            return self.action_to_reward[action]
        else:
            return 0

    def get_distr(self, action):
        if self.is_enabled(action):
            return self.action_to_succs[action]
        return None

    def is_enabled(self, action):
        return action in self.enabled_actions

    def __eq__(self, other):
        if isinstance(other, State):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.id

    def __repr__(self):
        return "State({},label={},id={})".format(self.name, self.label, self.id)

    def __str__(self):
        return self.name


def example1():
    mdp = MDP()
    s0 = mdp.add_state("s0")
    s1 = mdp.add_state("s1")
    s2 = mdp.add_state("s2")
    s3 = mdp.add_state("s3")
    s4 = mdp.add_state("s4")
    s5 = mdp.add_state("s5")
    mdp.add_edge(s0, s2, "a", p=0.5)
    mdp.add_edge(s0, s1, "a", p=0.5)
    mdp.add_edge(s2, s2, "a")
    mdp.add_edge(s1, s0, "a", p=0.5)
    mdp.add_edge(s1, s3, "a", p=0.5)
    mdp.add_edge(s3, s0, "a", p=0.5)
    mdp.add_edge(s3, s4, "a", p=0.5)
    mdp.add_edge(s4, s4, "a", p=0.25)
    mdp.add_edge(s4, s5, "a", p=0.75)
    mdp.add_edge(s4, s5, "b")
    mdp.add_edge(s5, s5, "a")
    vi = ValueIteration(mdp)
    vi.compute_reachability([s5], epsilon=0.01)
    vi.print_table()
    vi.print_action_table()


def example2():
    mdp = MDP()
    s0 = mdp.add_state("s0")
    s1 = mdp.add_state("s1")
    s2 = mdp.add_state("s2")
    mdp.add_edge(s0,s1,"a",p=0.5,reward=5)
    mdp.add_edge(s0,s0,"a",p=0.5,reward=5)
    mdp.add_edge(s1,s0,"a",p=0.999,reward=2)
    mdp.add_edge(s1,s2,"a",p=0.001,reward=2)
    mdp.add_edge(s2,s1,"c",reward=10)
    vi = ValueIteration(mdp)
    result = vi.compute_mean_payoff(epsilon=0.000001)
    mdp.to_dotty()
    print(result)


def example3():
    mdp = MDP()
    s0 = mdp.add_state("s0")
    s1 = mdp.add_state("s1")
    s2 = mdp.add_state("s2")
    mdp.add_edge(s0,s1,"a",p=0.001,reward=4)
    mdp.add_edge(s0,s0,"a",p=0.999,reward=4)
    mdp.add_edge(s1,s2,"a",reward=2)
    mdp.add_edge(s2,s1,"a",reward=2)
    vi = ValueIteration(mdp)
    mdp.to_dotty()
    result = vi.compute_mean_payoff(max_iter=10000)
    print(result)


def example4():
    mdp = MDP()
    s0 = mdp.add_state("s0")
    s1 = mdp.add_state("s1")
    s2 = mdp.add_state("s2")
    s3 = mdp.add_state("s3")
    s4 = mdp.add_state("s4")
    mdp.add_edge(s0, s1, "a", reward=5)
    mdp.add_edge(s1, s0, "a", p=0.5, reward=2)
    mdp.add_edge(s1, s2, "a", p=0.5, reward=2)
    mdp.add_edge(s2,s3, "b", p=0.5, reward=10)
    mdp.add_edge(s2,s2,"b",p=0.5,reward=10)
    mdp.add_edge(s3,s4,"a",reward=20)
    mdp.add_edge(s4,s3,"a",reward=20)
    mdp.to_dotty()

    print("Primal")
    lp = LPMeanPayoff(mdp)
    lp.compute(primal=True)

    print("Dual")
    lp = LPMeanPayoff(mdp)
    lp.compute(primal=False)

if __name__ == "__main__":
    example4()

    # mdp.to_dotty()
