"""
Tests the 'validate_time.py' in 'helpers'

"""

# imports
import unittest
import time
from time import sleep

from jsonWebToken.helpers import validate_time

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
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    #region 'tests'
    def test_validate_expiration(self):
        """Tests the validate_expiration function """

        print('WARNING: The test takes some time due to expiration checks!')

        #region 'exp is missing'
        result = validate_time.validate_expiration({})

        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "Not a JWT-Token from the 'jwt' package. Original error: KeyError: 'exp'")
        
        #endregion

        #region 'lifetime exeeced'
        payload = {'exp':int(time.time())}

        # sleep a second
        sleep(1)
        
        result = validate_time.validate_expiration(payload)

        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "Token expired.") 
        #endregion

        #region 'exp = None'
        payload = {'exp':None}

        # sleep a second
        sleep(1)
        
        result = validate_time.validate_expiration(payload)

        self.assertTrue(result['success'])

        #endregion

        #region 'success'
        payload = {'exp':int(time.time()) + 100}

        result = validate_time.validate_expiration(payload)

        self.assertTrue(result['success'])

        #endregion

    #endregion