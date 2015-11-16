
import os, time

from flask import Flask, render_template, session, escape, g, request, url_for, redirect, flash

app = Flask(__name__)
app.config.from_envvar('BOX_APPLICATION_SETTINGS')
app.config.from_object(__name__)

import logging_network

if app.config['DEBUG']:
    customLogger = logging_network.LoggingNetwork()
else:
    customLogger = None

from boxsdk import Client, JWTAuth
from boxsdk.object.user import User
from boxsdk.config import API

"""
Main Start


"""

# This should store the token in a cache and set the session value to a hashed retrieval key.
def store_tokens(access_t, refresh_t):
    session['token_id'] = access_t
    return

# When any request comes in, initialize the object that will check the expiration of the token.
# This object will also refresh the token against the API if needed.
@app.before_request
def load_auth_object_into_current_page_load_context():
    if "/static/" in request.path:
        return

    if "token_id" in session:
        print "ACCESS TOKEN FOUND: {0}".format(escape(session['token_id']))
        auth = JWTAuth(client_id=app.config['CLIENT_ID'],
            client_secret=app.config['CLIENT_SECRET'],
            enterprise_id=app.config['EID'],
            rsa_private_key_file_sys_path=os.path.join(os.path.dirname(__file__),'rsakey.pem'),
            store_tokens=store_tokens,
            access_token=escape(session['token_id'])) # <-- This is the difference
    else:
        auth = JWTAuth(client_id=app.config['CLIENT_ID'],
            client_secret=app.config['CLIENT_SECRET'],
            enterprise_id=app.config['EID'],
            rsa_private_key_file_sys_path=os.path.join(os.path.dirname(__file__),'rsakey.pem'),
            store_tokens=store_tokens)
        print "CREATED NEW ACCESS TOKEN: {0}".format(session['token_id'])
    g.auth = auth


@app.route('/')
def index():
    print '### Sending Index view ###'
    client = Client(g.auth, network_layer=customLogger)

    # NEVER SEND AN ADMIN TOKEN TO THE CLIENT
    # I only provide it here so that you can use this app to quickly get a token.
    return render_template("index.html",
                           users_list=client.users(),
                           groups_list=client.groups(),
                           token=g.auth.access_token)


@app.route('/user/<user_id>', methods=['GET'])
def user_detail(user_id):
    print '### Sending detail view ###'
    client = Client(g.auth, network_layer=customLogger)
    user = client.user(user_id=user_id).get()

    # As an admin, we can act on behalf of other users by creating new auth and client objects.
    # We should also be caching this token.  For the purposes of this quickstart
    # we only cache access for one user (the admin).
    print "AUTHENTICATING USER: " + user_id + " (" + user.name + ")"
    user_auth = JWTAuth(client_id=app.config['CLIENT_ID'],
                client_secret=app.config['CLIENT_SECRET'],
                enterprise_id=app.config['EID'],
                rsa_private_key_file_sys_path=os.path.join(os.path.dirname(__file__),'rsakey.pem'))
    user_auth.authenticate_app_user(user)
    user_client = Client(user_auth)

    # Do things as the user by using the user_client object
    files = user_client.folder(folder_id='0').get_items(limit=100)

    # Build the preview link into the file objects sent to the client
    for f in files:
        if f._item_type=="file":
            f.preview_url = f.get(fields=['expiring_embed_link']).expiring_embed_link['url']

    token = user_auth.access_token
    return render_template("detail.html",
                           user=user,
                           files_list=files,
                           token=token)


# During user creation we can create initial folder structures
# with retention policies, collaborations, etc.
@app.route('/user/new', methods=['POST'])
def create_user():
    if not request.form['name']:
        flash("Name required for user creation.", "error")
        return redirect(url_for('index'))
    client = Client(g.auth, network_layer=customLogger)
    new_user = client.create_user(request.form['name'],
                                  job_title=request.form['job'],
                                  phone=request.form['phone'],
                                  address=request.form['address'])
    if request.form.get('initialize'):
        # User init scripts go here
        add_user_to_group(client, new_user, "SuchGroup")
        flash("Initialized user: {0}".format(request.form['name']))
    else:
        flash("Created new user: {0} ".format(request.form['name']))

    return redirect(url_for('index'))

def add_user_to_group(client, user, groupname):
    [x.add_member(user, "member") for x in client.groups() if x.name==groupname]
    return

@app.route('/user/<user_id>', methods=['POST'])
def delete_user(user_id):
    if request.form['deleteconf'].lower() == 'yes':
        print "DELETING USER: {0}".format(user_id)
        flash("Deleted user: {0}".format(user_id))
        client = Client(g.auth, network_layer=customLogger)

        user = client.user(user_id=user_id)
        user.delete(params={"force":True}) # Use the force

        time.sleep(1) # Wait for the DB to catch up
        return redirect(url_for('index'))
    else:
        flash("Must type YES to confirm", 'error')
        return redirect(url_for('delete_user', user_id=user_id))


# Example direct call to the API
def listAllUsers(client):
    url = '{0}/users'.format(API.BASE_API_URL)
    box_response = client.make_request('GET', url)
    response = box_response.json()
    return [User(client._session, item['id'], item) for item in response['entries']]


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])