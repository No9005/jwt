"""
Contains functions to validate the expiration time
of a web token

"""

# imports
import datetime

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
        if token_content.header['exp'] is not None and token_content.header['exp'] != "None":

            # calculate expiration
            future = datetime.datetime.strptime(token_content.header['timestamp'], "%Y-%m-%d-%H-%M-%S-%f")

            # add exp time
            expiration = future + datetime.timedelta(seconds=int(token_content.header['exp']))

            # valid?
            if datetime.datetime.utcnow() > expiration: return {'success':False, 'error':"Token expired.", 'payload':{}}

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