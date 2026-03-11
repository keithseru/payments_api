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
    
    def test_returns_false_for_string(self):
        '''
        Returns false for a string
        '''
        self.assertFalse(validators.validateAmount("100"))

class ValidateCurrency(unittest.TestCase):
    def test_returns_true_three_string_char(self):
        '''
        Returns true for a three string character
        '''
        self.assertTrue(validators.validateCurrency('usd'))
    
    def test_returns_false_two_string_char(self):
        '''
        Returns false if the str has less than 3 chars
        '''
        self.assertFalse(validators.validateCurrency('us'))
    
    def test_returns_false_more_than_three_chars(self):
        '''
        Returns false if currency has more than three chars
        '''
        self.assertFalse(validators.validateCurrency('usdd'))
        
    def test_returns_false_for_empty_string(self):
        '''
        Returns false for empty string
        '''
        self.assertFalse(validators.validateCurrency('')) 
        
class ValidateEmail(unittest.TestCase):
    def test_retuns_true_for_contains_symbols(self):     
        '''
        Returns true if email contains @ and .
        '''
        self.assertTrue(validators.validateCurrency('alice@example.com'))
        
if __name__ == "__main__":
    unittest.main()