import unittest

from models.dtmc import DTMC
from pctl import AP, Disjunction, Conjunction, BoundedUntil, P
from utils import Interval


class PCTLTest(unittest.TestCase):

    def setUp(self) -> None:
        self.dtmc = DTMC()
        self.s0 = self.dtmc.add_state()
        self.s1 = self.dtmc.add_state()
        self.s2 = self.dtmc.add_state()
        self.dtmc.add_transition(self.s0, self.s1, 0.6)
        self.dtmc.add_transition(self.s0, self.s0, 0.3)
        self.dtmc.add_transition(self.s0, self.s2, 0.1)
        self.dtmc.add_transition(self.s2, self.s2, 1.0)
        self.dtmc.add_transition(self.s2, self.s0, 0.2)
        self.dtmc.add_transition(self.s2, self.s2, 0.8)
        self.a, self.b = AP("a"), AP("b")

    def test_disjunction(self):
        a, b = self.a, self.b
        self.s0.ap.append(a)
        self.s0.ap.append(b)
        self.s1.ap.append(a)
        self.s2.ap.append(b)
        phi = Disjunction(a, b)
        phi.eval(self.dtmc)
        self.assertIn(self.s0, phi.states)
        self.assertIn(self.s1, phi.states)
        self.assertIn(self.s2, phi.states)

    def test_conjunction(self):
        a, b = self.a, self.b
        self.s0.ap.append(a)
        self.s0.ap.append(b)
        self.s1.ap.append(a)
        self.s2.ap.append(b)
        phi = Conjunction(a, b)
        phi.eval(self.dtmc)
        self.assertIn(self.s0, phi.states)
        self.assertNotIn(self.s1, phi.states)
        self.assertNotIn(self.s2, phi.states)

    def test_bounded_until(self):
        a, b = self.a, self.b
        self.s2.ap.append(b)
        phi = P(Interval(0.1, 1.0), BoundedUntil(a, b, 10))
        phi.eval(self.dtmc)
        self.assertIn(self.s2, phi.states)
        self.s0.ap.append(self.a)

    def test_bounded_until_2(self):
        a, b = self.a, self.b
        self.s2.ap.append(b)
        self.s0.ap.append(self.a)
        psi = BoundedUntil(a, b, 2)
        prob = psi.compute_probability(self.s0, self.dtmc)
        self.assertAlmostEqual(prob, 0.13)


if __name__ == '__main__':
    unittest.main()
