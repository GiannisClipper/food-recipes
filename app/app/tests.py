from django.test import TestCase
from app.calc import add, subtrack


class CalcTests(TestCase):

    def test_add(self):
        """Test add function"""
        self.assertEqual(add(5, 6), 11)

    def test_subtrack(self):
        """Test subtrack function"""
        self.assertEqual(subtrack(5, 6), -1)
