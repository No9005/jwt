"""
Tests the rsa based token generation

"""

# imports
import unittest

from time import sleep

from jsonWebToken import with_rsa
from tests.key import rsa

#class
class TestWithRsa(unittest.TestCase):
    """Tests the functions from validate_time.py
    
    methods:
    --------
    setUp
        Test preparation
    tearDown
        Test result cleaning
    test_create_and_decode
        Tests creation and decoding of tokens
    
    """

    def setUp(self) -> None:

        self.maxDiff = None

    def tearDown(self) -> None:
        return super().tearDown()

    #region 'tests'
    def test_create_and_decode(self):
        """Tests the token creation & decoding """

        print('WARNING: The test takes some time due to expiration checks!')

        payload = {
            'sub': "1234567890", 
            'name': "John Doe",
            'admin': True,
            'iat': 0,
            'abc':None
        }

        #region 'success'
        token = with_rsa.create(
            payload = payload,
            private_key = rsa.private,
            expiration=100
        )

        result = with_rsa.decode(
            token,
            rsa.public
        )

        self.assertTrue(result['success'])

        pld = result['payload']
        del pld['exp']
        self.assertEqual(pld, payload)
        
        #endregion

        #region 'expired'
        token = with_rsa.create(
            payload = payload,
            private_key = rsa.private,
            expiration=1
        )

        sleep(2)

        result = with_rsa.decode(
            token,
            rsa.public
        )

        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "Token expired.")
        
        #endregion

        #region 'exp = none'
        token = with_rsa.create(
            payload = payload,
            private_key = rsa.private,
            expiration=None
        )

        sleep(1)

        result = with_rsa.decode(
            token,
            rsa.public
        )

        self.assertTrue(result['success'])
        
        #endregion

        #region 'exp = 0'
        token = with_rsa.create(
            payload = payload,
            private_key = rsa.private,
            expiration=0
        )

        result = with_rsa.decode(
            token,
            rsa.public
        )

        self.assertTrue(result['success'])
        
        #endregion

    #endregion