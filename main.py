import os, requests, json

from flask import Flask, render_template, redirect, url_for

from boxsdk.config import API
from boxsdk.object.user import User

import jwtAuth
from jwtAuth import *

app = Flask(__name__)

###
# 
# Steps on Github
# 
# Edit your ~/.bash_profile to include the following lines with your values
#   export BOX_SDK_CLIENTID=1234567890ABCD
#   export BOX_SDK_CLIENTSECRET=ABCDEFGHI1234
#   export BOX_SDK_EID=123456
###
# global client_id, client_secret, eid

### Example of how to make calls directly to the API after authentication
def listAllUsers(client):
    url = '{0}/users'.format(API.BASE_API_URL)
    box_response = client.make_request('GET', url)
    response = box_response.json()
    return [User(client._session, item['id'], item) for item in response['entries']]


###
# 1. Run the django server
#       python manage.py runserver
# 2. Navigate to localhost:8000/box/
#
###
@app.route('/')
def index():
    print 'Sending index view'
    initializeClientAndAuthObjects()



    ### Use this to create users (for now)
    # user = clientObject.create_user("Daniel Kaplan")

    token = jwtAuth.authObject.authenticate_instance()
    userList = jwtAuth.clientObject.users()

    print "### USER SEARCH: {0}".format(
        user_search(jwtAuth.clientObject, "Roger"))
    # context={
    #     "users_list":jwtAuth.clientObject.users(),
    #     "token":token
    # }
    return render_template("index.html", users_list=userList, token=token) ### Gets index.html from /box/templates/box/


def user_search(client, name, search_string):

    url = '{0}/users'.format(API.BASE_API_URL)
    headers = {'Content-Type': 'application/json'}

    # filters = [dict(name=name, op='like', val='%y%')]
    # params = dict(q=json.dumps(dict(filters=filters)))
    filters = [dict(name=name, op='like', val="%"+search_string+"%")]
    params = dict(q=json.dumps(dict(filters=filters)))

    response = requests.get(url, params=params, headers=headers)

    assert response.status_code == 200
    return response.json()

@app.route('/user/detail/<user_id>')
def detail(user_id):
    print 'Sending detail view'
    initializeClientAndAuthObjects()

    u = jwtAuth.clientObject.user(user_id=user_id).get() # Create a user object
    print "AUTHENTICATING AS USER: " + user_id + " (" + u.name + ")"
    user_token = jwtAuth.authObject.authenticate_app_user(u) # *****  Auth with that user to create folders ******
    user_client = Client(jwtAuth.authObject) # Create a new client for that user

    me = user_client.user(user_id='me').get() # Get the user's info

    ###
    ### Extra code for the detail view goes here
    ###

    ### Authenticate as the admin again
    print "AUTHENTICATING BACK TO ADMIN"
    jwtAuth.authObject.authenticate_instance()


    user = jwtAuth.clientObject.user(user_id=user_id).get() # Send the entire user json response
    token = user_token
    return render_template("detail.html", user=user, token=token)

#TODO
###
### Change to a form
###
def createUser(request, new_user_name):
    print 'Creating user'
    initializeClientAndAuthObjects()

    u = jwtAuth.clientObject.create_user(name=new_user_name)

    ###
    ### Initialization scripts go here
    ###



    return redirect(url_for('detail', u.id))

def deleteUser(request, user_id):
    initializeClientAndAuthObjects()

    u = jwtAuth.clientObject.user(user_id=user_id).get()
    u.delete()

    return


### CAREFUL WITH USAGE:
def deleteAll(request):
    ### DANGER: CANNOT BE UNDONE
    # print "Delete all App Users"
    # for u in clientObject.users():
    #     print u.delete()
    return "Uncomment the code first."





if __name__ == "__main__":
    app.run(debug=True)