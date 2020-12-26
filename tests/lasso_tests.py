import unittest
import numpy as np

from lasso.dtmc import DTMC


class MyTestCase(unittest.TestCase):
    def test_add_state(self):
        """Adding state"""
        dtmc = DTMC()
        s = dtmc.add_state("test")
        self.assertIn(s, dtmc.states, "States not added correctly")

    def test_transition_matrix(self):
        matrix = np.array([[0., 0.5, 0.5], [0., 1., 0.], [0., 0., 1.]])
        dtmc = DTMC()
        s1 = dtmc.add_state("s1")
        s2 = dtmc.add_state("s2")
        s3 = dtmc.add_state("s3")
        dtmc.add_transition(s1, 0.5, s2)
        dtmc.add_transition(s1, 0.5, s3)
        dtmc.add_transition(s2, 1, s2)
        dtmc.add_transition(s3, 1, s3)
        dtmc.compute_transition_matrix()
        self.assertTrue((matrix == dtmc.transition_matrix).all())

    def test_is_ergodic(self):
        dtmc = DTMC()
        s1 = dtmc.add_state("s1")
        s2 = dtmc.add_state("s2")
        dtmc.add_transition(s1, 1, s2)
        dtmc.add_transition(s2, 1, s1)
        self.assertFalse(dtmc.is_ergodic())
        dtmc = DTMC()
        s1 = dtmc.add_state("s1")
        s2 = dtmc.add_state("s2")
        dtmc.add_transition(s1, 0.5, s2)
        dtmc.add_transition(s2, 0.5, s1)
        dtmc.add_transition(s1,0.5,s1)
        dtmc.add_transition(s2,0.5,s2)
        self.assertTrue(dtmc.is_ergodic())


if __name__ == '__main__':
    unittest.main()
