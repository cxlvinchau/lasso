import unittest
from lasso.pctl import parse, AP, Conjunction, Disjunction, Negation


class ParserTest(unittest.TestCase):
    def test_parse_ap(self):
        ap = parse("a")
        self.assertIsInstance(ap, AP)
        self.assertEqual(ap.symbol, "a")

    def test_parse_conjunction(self):
        conjunction = parse("a & b")
        self.assertIsInstance(conjunction, Conjunction)
        self.assertIsInstance(conjunction.phi1, AP)
        self.assertIsInstance(conjunction.phi2, AP)
        self.assertEqual(conjunction.phi1.symbol, "a")
        self.assertEqual(conjunction.phi2.symbol, "b")

    def test_parse_disjunction(self):
        disjunction = parse("a | b")
        self.assertIsInstance(disjunction, Disjunction)
        self.assertIsInstance(disjunction.phi1, AP)
        self.assertIsInstance(disjunction.phi2, AP)
        self.assertEqual(disjunction.phi1.symbol, "a")
        self.assertEqual(disjunction.phi2.symbol, "b")

    def test_parse_negation(self):
        neg = parse("!a")
        self.assertIsInstance(neg, Negation)


if __name__ == '__main__':
    unittest.main()
