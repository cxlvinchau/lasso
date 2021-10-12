from lasso.models import DTMC
from lasso.pctl import AP, parse

# Create DTMC
dtmc = DTMC()

# Add states
s1 = dtmc.add_state("s1")
s1.ap.append(AP("a"))
s2 = dtmc.add_state("s2")
s2.ap.append((AP("a")))
s3 = dtmc.add_state("s3")
s3.ap.append(AP("b"))
s4 = dtmc.add_state()

# Add transitions
dtmc.add_transition(s1, s3, 0.1)
dtmc.add_transition(s1, s2, 0.6)
dtmc.add_transition(s2, s2, 0.8)
dtmc.add_transition(s2, s1, 0.2)
dtmc.add_transition(s3, s3, 1.0)
dtmc.add_transition(s1, s4, 0.3)
dtmc.add_transition(s4, s4, 1.0)

# Print DTMC as dot
print(dtmc.to_dot())

# PCTL Model Checking
phi = parse("P[0.9,1.0](a U b)")
print(phi)
phi.eval(dtmc)
print(phi.states)

print(dtmc.compute_reachability([s3]))