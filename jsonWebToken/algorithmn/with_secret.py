"""
Collection of functions which encodes and
decodes a jws created with a secret (HS256).

"""

# import 
import time
import json

from authlib.jose import JsonWebSignature

from jsonWebToken.helpers.validate_time import validate_expiration

#region 'functions' ----------------------------
def create(payload:dict, secret:str, expiration:int = 600) -> str:
    """This function creates a HS256 signed token.
    
    params:
    -------
    payload : dict
        Jsonifyable dict.
    secret : str
        Secret to use to sign the token.
            Caution: secret will be 'utf-8'
                     encoded prior using.
    expiration : int, optional
        The time in seconds after the token
        expires.
        (default is 600)
            Caution: If the value is 0, the
                     token is always valid
    
    returns:
    --------
    JWT-token
        The token containing the payload.
        
    """

    # get current time in utc
    now = int(time.time())

    # parse expiration
    exp = None
    if expiration is not None:
        if expiration <= 0: exp=None
        else: exp = now + expiration

    # encode secret
    sec = secret.encode('utf-8')

    # create jwt instance
    jwt = JsonWebSignature(algorithms="HS256")

    # build the token
    token = jwt.serialize_compact(
        {
            'alg':"HS256", 'type':"JWT"
        },
        json.dumps({
            'exp':exp,
            'iat':now,
            **payload
        }),
        sec
    )

    return token

def decode(token:str, secret:str) -> dict:
    """Decodes a 'JWT'-Token 
    
    params:
    -------
    token : str
        The JWT-created token.
    secret : str
        Secret used to sign the
        token (during creation).

    returns:
    -------
    dict
        Dictionary containing info about
        success, error & payload.
    
    """

    # create instance
    jwt = JsonWebSignature(algorithms="HS256")

    # encode secret
    secretByte = secret.encode('utf-8')
    
    # decode
    try: content = jwt.deserialize_compact(token, secretByte)
    except Exception as e: return {'success':False, 'error':"{t}: {m}".format(t=str(type(e).__name__), m=str(e)), 'payload':{}}

    # alg == HS256?
    if not content.header['alg'] == "HS256": return {'success':False, 'error':"Wrong 'alg'."}

    # get payload
    payload = json.loads(content.payload)

    # validate timestamp
    valid = validate_expiration(payload)
    if not valid['success']: return valid

    # all done?
    return {
        'success':True,
        'error':"",
        'payload':payload
    }

#endregion