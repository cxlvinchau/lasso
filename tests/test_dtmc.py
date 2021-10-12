import unittest
import numpy as np

from lasso.models.dtmc import DTMC


class TestDTMC(unittest.TestCase):

    def setUp(self) -> None:
        self.dtmc = DTMC()

    def test_add_state(self):
        self.dtmc.add_state()
        self.assertEqual(len(self.dtmc.states), 1)

    def test_add_transition(self):
        s1 = self.dtmc.add_state()
        s2 = self.dtmc.add_state()
        t = self.dtmc.add_transition(s1, s2, 0.5)
        self.assertEqual(len(self.dtmc.transitions), 1)

    def test_compute_transition_matrix(self):
        s1 = self.dtmc.add_state()
        s2 = self.dtmc.add_state()
        t = self.dtmc.add_transition(s1, s2, 0.5)
        self.dtmc.compute_transition_matrix()
        self.assertTrue(np.allclose(self.dtmc.transition_matrix, np.array([[0.0, 0.5], [0.0, 0.0]])))

    def test_compute_transient(self):
        s1 = self.dtmc.add_state()
        s2 = self.dtmc.add_state()
        self.dtmc.add_transition(s1, s2, 0.5)
        self.dtmc.add_transition(s1, s1, 0.5)
        self.dtmc.add_transition(s2, s2, 1.0)
        res = self.dtmc.transient(1, np.array([1.0, 0]))
        self.assertTrue(np.allclose(res, np.array([0.5, 0.5])))
        res = self.dtmc.transient(2, {s1: 1.0})
        self.assertTrue(np.allclose(res, np.array([0.25, 0.75])))

    def test_compute_reachability(self):
        s1 = self.dtmc.add_state()
        s2 = self.dtmc.add_state()
        self.dtmc.add_transition(s1, s2, 0.5)
        self.dtmc.add_transition(s1, s1, 0.5)
        self.dtmc.add_transition(s2, s2, 1.0)
        res = self.dtmc.compute_reachability([s1], steps=10)
        self.assertAlmostEqual(res[s1.id], 1.0)
        self.assertAlmostEqual(res[s2.id], 0.0)
        res = self.dtmc.compute_reachability([s2], steps=100)
        self.assertAlmostEqual(res[s1.id], 1.0)
        self.assertAlmostEqual(res[s2.id], 1.0)
        res = self.dtmc.compute_reachability([s2], bad_states=[s1], steps=100)
        self.assertAlmostEqual(res[s1.id], 0.0)
        self.assertAlmostEqual(res[s2.id], 1.0)

    def test_to_dot(self):
        s1 = self.dtmc.add_state()
        s2 = self.dtmc.add_state()
        t = self.dtmc.add_transition(s1, s2, 0.5)
        t = self.dtmc.add_transition(s1, s1, 0.5)
        t = self.dtmc.add_transition(s2, s2, 1.0)
        s = self.dtmc.to_dot()
        print(s)

    def test_unbounded_reachability(self):
        s1 = self.dtmc.add_state()
        s2 = self.dtmc.add_state()
        t = self.dtmc.add_transition(s1, s2, 0.5)
        t = self.dtmc.add_transition(s1, s1, 0.5)
        t = self.dtmc.add_transition(s2, s2, 1.0)
        v = self.dtmc.compute_reachability([s2])
        self.assertAlmostEqual(v[s1.id], 1.0)


if __name__ == '__main__':
    unittest.main()
