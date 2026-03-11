import unittest
from app.utils import validators

class ValidateAmount(unittest.TestCase):
    def test_returns_true_amount_positive(self):
        '''
        Returns true if amount is a positive integer
        '''
        self.assertTrue(validators.validate_amount(100))
    
    def test_returns_false_amount_negative(self):
        '''
        Returns false if amount is a negative integer
        '''
        self.assertFalse(validators.validate_amount(-1))
    
    def test_edge_test_minimum_boundary(self):
        '''
        Returns true for minimum boundary 1
        '''
        self.assertTrue(validators.validate_amount(1))
    
    def test_edge_test_0(self):
        '''
        Returns false for amount 0
        '''
        self.assertFalse(validators.validate_amount(0))
    
    def test_returns_false_for_decimal(self):
        '''
        Returns false for decimal number
        '''
        self.assertFalse(validators.validate_amount(9.99))
    
    def test_returns_false_for_null(self):
        '''
        Returns false for null
        '''
        self.assertFalse(validators.validate_amount(None))
    
    def test_returns_false_for_string(self):
        '''
        Returns false for a string
        '''
        self.assertFalse(validators.validate_amount("100"))

class ValidateCurrency(unittest.TestCase):
    def test_returns_true_three_string_char(self):
        '''
        Returns true for a three string character
        '''
        self.assertTrue(validators.validate_currency('usd'))
    
    def test_returns_false_two_string_char(self):
        '''
        Returns false if the str has less than 3 chars
        '''
        self.assertFalse(validators.validate_currency('us'))
    
    def test_returns_false_more_than_three_chars(self):
        '''
        Returns false if currency has more than three chars
        '''
        self.assertFalse(validators.validate_currency('usdd'))
        
    def test_returns_false_for_empty_string(self):
        '''
        Returns false for empty string
        '''
        self.assertFalse(validators.validate_currency('')) 
        
class ValidateEmail(unittest.TestCase):
    def test_retuns_true_for_contains_symbols(self):     
        '''
        Returns true if email contains @ and .
        '''
        self.assertTrue(validators.validate_email('alice@example.com'))
    
    def test_returns_false_missing_symbol(self):
        '''
        Returns False if @ is missing in email
        '''
        self.assertFalse(validators.validate_email('aliceexample.com'))
    
    def test_returns_false_for_empty_string(self):
        '''
        Returns false if string is empty
        '''
        self.assertFalse(validators.validate_email(""))
    
class GenerateIdTests(unittest.TestCase):
    def test_returns_string_starting_with_prefix(self):
        result = validators.generate_id("pay")
        self.assertTrue(result.startswith("pay_"))
    
    def test_returns_different_value_on_each_call(self):
        result1 = validators.generate_id("pay")
        result2 = validators.generate_id("pay")
        self.assertNotEqual(result1, result2)
        
if __name__ == "__main__":
    unittest.main()