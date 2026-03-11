import unittest
from app.utils import validators

class ValidateAmount(unittest.TestCase):
    def test_returns_true_amount_positive(self):
        '''
        Returns true if amount is a positive integer
        '''
        self.assertTrue(validators.validateAmount(100))
    
    def test_returns_false_amount_negative(self):
        '''
        Returns false if amount is a negative integer
        '''
        self.assertFalse(validators.validateAmount(-1))
    
    def test_edge_test_minimum_boundary(self):
        '''
        Returns true for minimum boundary 1
        '''
        self.assertTrue(validators.validateAmount(1))
    
    def test_edge_test_0(self):
        '''
        Returns false for amount 0
        '''
        self.assertFalse(validators.validateAmount(0))
    
    def test_returns_false_for_decimal(self):
        '''
        Returns false for decimal number
        '''
        self.assertFalse(validators.validateAmount(9.99))
    
    def test_returns_false_for_null(self):
        '''
        Returns false for null
        '''
        self.assertFalse(validators.validateAmount(None))

if __name__ == "__main__":
    unittest.main()