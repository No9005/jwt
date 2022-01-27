"""
Tests the rsa based token generation

"""

# imports
import unittest

from time import sleep

from jsonWebToken import with_secret
#class
class TestWithSecret(unittest.TestCase):
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
        return super().setUp()

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
        token = with_secret.create(
            payload = payload,
            secret = "mySignatureKey",
            expiration=100
        )

        result = with_secret.decode(
            token,
            secret = "mySignatureKey"
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['payload'], payload)
        
        #endregion

        #region 'expired'
        token = with_secret.create(
            payload = payload,
            secret = "mySignatureKey",
            expiration=1
        )

        sleep(1)

        result = with_secret.decode(
            token,
            secret = "mySignatureKey"
        )

        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "Token expired.")
        
        #endregion

        #region 'exp = none'
        token = with_secret.create(
            payload = payload,
            secret = "mySignatureKey",
            expiration=None
        )

        sleep(1)

        result = with_secret.decode(
            token,
            secret = "mySignatureKey"
        )

        self.assertTrue(result['success'])
        
        #endregion

        #region 'exp = 0'
        token = with_secret.create(
            payload = payload,
            secret = "mySignatureKey",
            expiration=0
        )

        result = with_secret.decode(
            token,
            secret = "mySignatureKey"
        )

        self.assertTrue(result['success'])
        
        #endregion

    #endregion