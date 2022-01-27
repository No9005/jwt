"""
Collection of functions which encode and decode
jwt with an public & private rsa key (RS256).

"""

# import 
import datetime

from authlib.jose import JsonWebToken

from jsonWebToken.helpers.validate_time import validate_expiration

#region 'functions' ----------------------------
def create(payload:dict, private_key:str, expiration:int = 600) -> str:
    """This function creates a RS256 signed token.
    
    params:
    -------
    payload : dict
        Jsonifyable dict.
    private_key : str
        The loaded rsa-private-key from the
        '.pem' file.
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

    # parse expiration
    exp = expiration
    if expiration is not None:
        if expiration <= 0: exp=None

    # get current time in utc
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S-%f")

    # create jwt instance
    jwt = JsonWebToken(algorithms="RS256")

    # build the token
    token = jwt.encode(
        {
            'alg':"RS256", 'type':"JWT", 'exp':exp, 'timestamp':now
        },
        payload,
        private_key
    )

    return token

def decode(token:str, public_key:str) -> dict:
    """Decodes a 'JWT'-Token 
    
    params:
    -------
    token : str
        The JWT-created token.
    public_key : str
        The public rsa key.

    returns:
    -------
    dict
        Dictionary containing info about
        success, error & payload.
    
    """

    # create instance
    jwt = JsonWebToken(algorithms="RS256")
    
    # decode
    try: content = jwt.decode(token, public_key)
    except Exception as e: return {'success':False, 'error':"{t}: {m}".format(t=str(type(e).__name__), m=str(e)), 'payload':{}}

    # validate timestamp
    valid = validate_expiration(content)
    if not valid['success']: return valid

    # all done?
    return {
        'success':True,
        'error':"",
        'payload':content
    }

#endregion