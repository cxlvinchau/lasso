import gurobipy as grb
from gurobipy import GRB

class LPMeanPayoff:

    def __init__(self,mdp):
        self.mdp = mdp

    def compute(self,primal=True):
        if primal:
            self._compute_primal()
        else:
            self._compute_dual()

    def _compute_dual(self):
        with grb.Env(empty=True) as env:
            env.setParam('LogToConsole', 0)
            env.start()
            with grb.Model(env=env) as model:
                keys = {}
                for s in self.mdp.states:
                    for a in s.enabled_actions:
                        keys[(s,a)] = s.get_reward(a)
                x = model.addVars(keys,vtype=GRB.CONTINUOUS)
                y = model.addVars(keys,vtype=GRB.CONTINUOUS)
                for s in self.mdp.states:
                    transitions = [t for t in self.mdp.transitions if t.target == s]
                    actions = {(t.source,t.action): t.p for t in transitions}
                    enabled = [(s,a) for a in s.enabled_actions]
                    # Constraint of type 1
                    model.addConstr(1 + sum(actions[a] * y[a] for a in actions) >= sum(y[a] for a in enabled) + sum(x[a] for a in enabled))
                    # Constraint of type 2
                    model.addConstr(sum(actions[a] * x[a] for a in actions) == sum(x[a] for a in enabled))
                # Set objective function
                model.setObjective(sum(keys[k] * x[k] for k in keys),GRB.MAXIMIZE)
                model.optimize()
                # Print solution
                x_sum = sum(x[k].x for k in keys)
                y_sum = sum(y[k].x for k in keys)
                for k in keys:
                    print("x_{} = {}".format(k,x[k].x/x_sum))
                for k in keys:
                    print("y_{} = {}".format(k,y[k].x/y_sum))
                print("Mean payoff: {}".format(sum(keys[k] * x[k].x/x_sum for k in keys)))


    def _compute_primal(self):
        with grb.Env(empty=True) as env:
            env.setParam('LogToConsole', 0)
            env.start()
            with grb.Model(env=env) as model:
                x = model.addVars([s for s in self.mdp.states],vtype=GRB.CONTINUOUS)
                y = model.addVars([s for s in self.mdp.states],vtype=GRB.CONTINUOUS)
                for s in self.mdp.states:
                    for a in s.enabled_actions:
                        distr = s.get_distr(a)
                        model.addConstr(x[s] >= sum(distr[u]*x[u] for u in distr))
                        model.addConstr(x[s] >= s.get_reward(a) + sum(distr[u]*y[u] for u in distr) - y[s])
                model.setObjective(sum(x[s] for s in self.mdp.states),GRB.MINIMIZE)
                model.optimize()
                print("Value:")
                for s in self.mdp.states:
                    print("x({}) = {}".format(s,x[s].x))
                print("Y variables")
                for s in self.mdp.states:
                    print("y({}) = {}".format(s,y[s].x))
