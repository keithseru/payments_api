import unittest
from app.utils import validateAmount

class ValidateAmount(unittest.TestCase):
    def test_returns_true_amount_positive():
        '''
        Returns true if amount is a positive integer
        '''
        assert validateAmount(100) is True

if __name__ == "__main__":
    unittest.main()