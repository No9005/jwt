"""
Tests the 'validate_time.py' in 'helpers'

"""

# imports
import unittest
import datetime
from time import sleep

from jsonWebToken.helpers import validate_time

#region 'create cls fake class'
class CLS:
    def __init__(self, header:dict={}) -> None:
        self.header = header

#endregion

#class
class TestValidateTime(unittest.TestCase):
    """Tests the functions from validate_time.py
    
    methods:
    --------
    setUp
        Test preparation
    tearDown
        Test result cleaning
    test_validate_expiration
        Test the expiration checks
    
    """

    def setUp(self) -> None:
        
        self.content = CLS()

    def tearDown(self) -> None:
        return super().tearDown()

    #region 'tests'
    def test_validate_expiration(self):
        """Tests the validate_expiration function """

        print('WARNING: The test takes some time due to expiration checks!')

        #region 'exp is missing'
        result = validate_time.validate_expiration(self.content)

        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "Not a JWT-Token from the 'jwt' package. Original error: KeyError: 'exp'")
        
        #endregion

        #region 'datetime in wrong format'
        self.content.header = {'exp':100, 'timestamp':'%1900-%3-%1-%5-%3'}
        
        result = validate_time.validate_expiration(self.content)

        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "Not a JWT-Token from the 'jwt' package. Original error: ValueError: time data '%1900-%3-%1-%5-%3' does not match format '%Y-%m-%d-%H-%M-%S-%f'")
        
        #endregion

        # get now
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S-%f")

        #region 'lifetime exeeced'
        self.content.header = {'exp':1, 'timestamp':now}

        # sleep a second
        sleep(1)
        
        result = validate_time.validate_expiration(self.content)

        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "Token expired.") 
        #endregion

        #region 'exp = None'
        self.content.header = {'exp':None, 'timestamp':now}

        # sleep a second
        sleep(1)
        
        result = validate_time.validate_expiration(self.content)

        self.assertTrue(result['success'])

        #endregion

        #region 'success'
        self.content.header = {'exp':100, 'timestamp':now}

        result = validate_time.validate_expiration(self.content)

        self.assertTrue(result['success'])

        #endregion

    #endregion