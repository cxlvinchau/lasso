from tabulate import tabulate
import matplotlib.pyplot as plt

class ValueIteration:

    def __init__(self, mdp):
        self.mdp = mdp
        self.table = None
        self.action_table = None

    def compute_reachability(self, targets, bound=None, epsilon=0.01):
        init = {s: (1 if s in targets else 0) for s in self.mdp.states}
        table = [init]
        action_table = []
        step = 1
        while True:
            # Stopping criterion
            if bound is None and step >= 2:
                max_diff = max(abs(table[-1][s]-table[-2][s]) for s in self.mdp.states)
                if max_diff <= epsilon:
                    break
            elif bound is not None and step > bound:
                break

            value_row = {}
            action_row = {}
            for s in self.mdp.states:
                max_action = None
                max_value = 0
                for action in s.enabled_actions:
                    distr = s.get_distr(action)
                    row = table[-1]
                    value = sum(row[u] * distr[u] for u in distr)
                    if value >= max_value:
                        max_value = value
                        max_action = action
                value_row[s] = max_value
                action_row[s] = max_action
            table.append(value_row)
            action_table.append(action_row)
            step += 1
        self.table = table
        self.action_table = action_table

    def compute_mean_payoff(self,max_iter=None,epsilon=0.01):
        w = {s: 0 for s in self.mdp.states}
        u_list = []
        l_list = []
        iter = 0
        while True:
            w_old = w
            w = dict()
            for s in self.mdp.states:
                max_value = 0
                for action in s.enabled_actions:
                    distr = s.get_distr(action)
                    value = s.get_reward(action) + sum(distr[u]*w_old[u] for u in distr)
                    max_value = max(max_value,value)
                w[s] = max_value
            upper = max(w[s]-w_old[s] for s in self.mdp.states)
            lower = min(w[s]-w_old[s] for s in self.mdp.states)
            u_list.append(upper)
            l_list.append(lower)
            iter += 1
            if max_iter is None and upper - lower <= epsilon:
                break
            if max_iter is not None and iter > max_iter:
                break
        plt.plot([i for i in range(1,len(u_list)+1)],u_list,label="Upper")
        plt.plot([i for i in range(1,len(l_list)+1)],l_list,label="Lower")
        plt.legend()
        plt.title("Value iteration")
        plt.xlabel("Iteration")
        plt.ylabel("Reward")
        plt.show()
        return (upper+lower)/2

    def print_table(self):
        print("Value table")
        if self.table is None:
            return
        result = [[index] + [row[s] for s in self.mdp.states] for index,row in enumerate(self.table)]
        print(tabulate(result,headers=["Iteration"] + [s for s in self.mdp.states]))

    def print_action_table(self):
        print("Action table")
        if self.action_table is None:
            return
        result = [[index+1] + [row[s] for s in self.mdp.states] for index,row in enumerate(self.action_table)]
        print(tabulate(result,headers=["Iteration"] + [s for s in self.mdp.states]))


