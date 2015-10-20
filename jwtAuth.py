__author__ = 'danielkaplan'

import os
from boxsdk import Client, JWTAuth
import logging_network

client_id = os.environ.get('BOX_SDK_CLIENTID') # Your Client ID
client_secret = os.environ.get('BOX_SDK_CLIENTSECRET') # Your Client Secret
eid = os.environ.get('BOX_SDK_EID') # Enterprise ID number

# These will be set on Authentication
access_token = ""
refresh_token = ""

# These will be used to refresh the token if needed
authObject = None
clientObject = None

customLogger = None


def initializeClientAndAuthObjects():
    ######
    ######
    # IMPORTANT: You will need to place your RSA private key in /box/rsakey.pem
    ######
    ######
    global authObject
    try:
        authObject
    except NameError:
        authObject = None
    if authObject is None:
        print "refreshing auth "
        authObject = JWTAuth(client_id=client_id,
            client_secret=client_secret,
            enterprise_id=eid,
            rsa_private_key_file_sys_path=os.path.join(os.path.dirname(__file__),'rsakey.pem'),
            store_tokens=store_tokens)

    ### If you don't want the logging, use the line after it.
    global clientObject
    try:
        clientObject
    except NameError:
        clientObject = None
    if clientObject is None:
        print "refreshing client "
        clientObject = Client(authObject, network_layer=getLogger())
        print "initializing " + clientObject.__str__()
        # clientObject = Client(authObject)
    return

### Called by the authentication method.
def store_tokens(access_t, refresh_t):
    global access_token, refresh_token
    access_token=access_t
    refresh_token=refresh_t

    ### The SDK will refresh the token if/when it expires.
    ### This token will work for testing with PostMan or curl or others
    print "Access Token: {0}".format(access_token)
    ### JWT does not have refresh tokens.  This will be the Python type 'None'
    print "Refresh Token: {0}".format(refresh_token)
    return

def getLogger():
    global customLogger
    try:
        customLogger
    except NameError:
        customLogger = None
    if customLogger is None:
        customLogger=logging_network.LoggingNetwork()
    return customLogger

