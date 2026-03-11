import unittest
from app.utils import validators

class ValidateAmount(unittest.TestCase):
    def test_returns_true_amount_positive():
        '''
        Returns true if amount is a positive integer
        '''
        assert validators.validateAmount(100) is True

if __name__ == "__main__":
    unittest.main()