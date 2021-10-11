import lark

from lasso.pctl.pctl_ import TT, AP, Disjunction, StateFormula, Conjunction, Negation, P, Next, BoundedUntil, Until
from lasso.utils import Interval

GRAMMAR = r"""
?state_formula: "true" -> true | ap | disjunction | conjunction | neg state_formula -> negation | "P" range "("path_formula")" -> probability | "(" state_formula ") -> brackets"
?path_formula: "X" state_formula -> next | state_formula "U" state_formula -> until | state_formula "U<="INT state_formula -> bounded_until
disjunction.1: state_formula "|" state_formula
conjunction.2: state_formula "&" state_formula
neg : "!"

CMP: ">=" | "==" | "<="
ap: LCASE_LETTER
range: CMP DECIMAL -> comparison | "["DECIMAL","DECIMAL"]" -> interval

%import common.LCASE_LETTER
%import common.DECIMAL
%import common.INT
"""

PCTL_PARSER = lark.Lark(GRAMMAR, start="state_formula")

class PCTLTransformer(lark.Transformer):

    # State formulae
    def true(self, _):
        return TT()

    def ap(self, symbol):
        return AP(symbol[0].value)

    def disjunction(self, values):
        return Disjunction(*values)

    def conjunction(self, values):
        return Conjunction(*values)

    def negation(self, values):
        return Negation(values[1])

    def probability(self, values):
        return P(*values)

    def brackets(self, value):
        return value

    # Path formulae
    def next(self, values):
        return Next(values[0])

    def bounded_until(self, values):
        phi1, bound, phi2 = values
        return BoundedUntil(phi1, phi2, int(bound))

    def until(self, values):
        return Until(*values)

    # Utilities
    def interval(self, bounds):
        return Interval(bounds[0].value, bounds[1].value)

    def comparison(self, values):
        cmp, bound = values
        if cmp.value == "==":
            return Interval(bound.value, bound.value)
        if cmp.value == "<=":
            return Interval(0.0, bound.value)
        if cmp.value == ">=":
            return Interval(bound.value, 1.0)


PCTLTransformer = PCTLTransformer()


def parse(s: str):
    """Parses a string into a PCTL formula"""
    tree = PCTL_PARSER.parse(s.replace(" ", ""))
    return PCTLTransformer.transform(tree)

