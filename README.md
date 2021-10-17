# lasso
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Tests](https://github.com/cxlvinchau/lasso/actions/workflows/tests.yml/badge.svg)](https://github.com/cxlvinchau/lasso/actions/workflows/tests.yml)

Simple analysis and model checking tool for finite discrete time-homogeneous Markov chains (DTMC). 
Model checks PCTL properties and computes transient distribution.

In traditional model checking and automata theory, a lasso refers to the infinite part of a sequence accepted by an automaton (e.g. Büchi).

## Installation
Simply clone this repository, navigate into the repository and run:
```
pip install -e .
```

## Usage

### Creating a DTMC
```
from lasso.models import DTMC
from lasso.pctl import AP
# Create model
dtmc = DTMC()

# Add states
s1 = dtmc.add_state()
s2 = dtmc.add_state()

# Add transitions
t = self.dtmc.add_transition(s1, s2, 0.5)
t = self.dtmc.add_transition(s1, s1, 0.5)
t = self.dtmc.add_transition(s2, s2, 1.0)

# Add atomic proposition to state
s1.ap.append(AP("a"))
s2.ap.append(AP("b"))
```

### Plotting DTMC
```
dtmc.to_dot()
```

### PCTL
```
from lasso.pctl import AP, Disjunction, Conjunction, BoundedUntil, P
from lasso.utils import Interval
a, b = AP("a"), AP("b")

# P[0.5, 1.0]((a or b) U b)
P(Interval(0.5, 1.0), Until(Disjunction(a, b), b))

# P[0.5, 1.0](X b)
P(Interval(0.5, 1.0), Next(b))
```
Alternatively it is also possible to parse a PCTL formula according to the following grammar:
```
state_formula -> state_formula & state_formula
              -> state_formula | state_formula
              -> P[float, float](path_formula)
              -> !state_formula
              -> (state_formula)
              -> ap
              
path_formula -> X state_formula
             -> state_formula U state_forumla
             -> state_formula U<=integer state_forumla
```
``ap`` can be any lowercase letter and ``float`` is supposed to be floating number between 0 and 1.
Correspondingly, ``integer`` needs to be an integer number.

**Parsing formula from string**
```
from lasso.pctl import parse

# Results in Conjunction(a, b)
phi = parse("a & b")
```

## Background
This tool is based on the material of the **Quantitative Verification** course at the Technical University of Munich (TUM).
