import unittest
from app.utils import validators

class ValidateAmount(unittest.TestCase):
    def test_returns_true_amount_positive(self):
        '''
        Returns true if amount is a positive integer
        '''
        self.assertTrue(validators.validateAmount(100))

if __name__ == "__main__":
    unittest.main()