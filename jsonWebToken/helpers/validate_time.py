"""
Contains functions to validate the expiration time
of a web token

"""

# imports
import time

#functions
def validate_expiration(token_content):
    """Checks if the token is still valid
    
    params:
    ------
    token_content : jwt cls
        The authlib claims_cls object
    
    returns:
    --------
    dict
        success:bool, error:str &
        payload:dict

    """

    # expiration check
    try:
        # check if we need to validate expiration
        if token_content['exp'] is not None and token_content['exp'] != "None":

            # valid?
            if int(time.time()) > int(token_content['exp']): return {'success':False, 'error':"Token expired.", 'payload':{}}

    except Exception as e: 
        
        msg = "Not a JWT-Token from the 'jwt' package. Original error: {t}: {m}".format(
            t=str(type(e).__name__), 
            m=str(e)
            )

        return {'success':False, 'error':msg, 'payload':{}}

    # did all work?
    return {
        'success':True,
        'error':"",
        'payload':{}
    }