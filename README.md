# Box App Users - Python/Flask Quickstart
Code is commented. Everything important is in /main.py  
Box Docs - <https://docs.box.com/docs/overview>   
Box API Reference - <https://docs.box.com/reference>

### Step 0: Setup virtualenv & Install packages   
It's always recommended to use [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) with Python  
Use python 2.7.*  **Note: Does not work with 3.x**  

0.1 Create and setup a virtualenv:   
Note**: The Virtual Environment folder "boxpythonruntime" will be a created in the current folder
```
sudo pip install virtualenv
virtualenv pythonruntime && source pythonruntime/bin/activate && pip install -U setuptools wheel && pip install -U pip && pip install -U boxsdk[jwt]
```

0.2 To exit the virtual environment:
```
deactivate
```

0.3 To use the virtualenv again:
```
source pythonruntime/bin/activate
```


### Step 1: Pull code  
Note: First navigate to the folder you want to place /boxflaskjwt/
```
git clone https://github.com/dann815/boxflaskjwt.git  
cd boxflaskjwt
```


### Step 2: Generate your RSA keys  
2.1 Create a private key…  
... with a password:  
```
openssl genrsa -aes256 -out rsakey.pem 2048
```  
... or without a password:  
```
openssl genrsa -out rsakey.pem 2048 
```  
**NOTE: DO NOT COMMIT KEY FILE TO ANY PUBLIC LOCATIONS.  This code assumes the private key is in the project's folder.

2.2 Create a public key from the private key:  
```
openssl rsa -pubout -in rsakey.pem -out rsapublic.pem  
```


### Step 3: Input your RSA keys into Box Developer Console
3.0 Log in (upper right corner) to the Box Developer Console at <http://developer.box.com>
Create an app (right sidebar).
Under "OAuth2 Parameters", select the Authentication Type with JWT.


3.1 Copy your public key:  
```
cat rsapublic.pem | pbcopy  
```

3.2 Add the public key to your application. CLICK SAVE!
If you need help, follow the instructions at: <https://box-content.readme.io/v2.0/docs/app-auth>  


### Step 4: Configuration  
4.1 Create a file named settings.cfg   
```
touch settings.cfg
```

4.2 Generate and copy a random string: 
```
python
import os
os.urandom(24)
exit()
```  


4.3 Open a text editor and add the following lines to settings.cfg:  
```
open -e settings.cfg
```
Copy this into the file:
```
# General config
DEBUG = True
SECRET_KEY = 'A RANDOM SECRET KEY'

# Box config
CLIENT_ID = 'YOUR CLIENT ID'
CLIENT_SECRET = 'YOUR CLIENT SECRET'
EID = 'YOUR BOX ENTERPRISE ID'
``` 
Fill in the values.  Your CLIENT_ID and CLIENT_SECRET are in the Box Developer Console where you just made your application.  

To get your Box Enterprise ID:
1) Click "Admin Console" in the upper left corner.
2) Click the gear icon in the upper right corner
3) Click the first option (Business/Enterprise Settings)
4) Account Information -> Enterprise ID

  
4.4 Set the environment variable to point to the full path location of the settings.cfg file  
```
export BOX_APPLICATION_SETTINGS=/FULL/PATH/TO/settings.cfg
```

### Step 5: Run the code  
5.1 Run:
```
python main.py  
```
5.2 Navigate to:  
<http://localhost:5000> 



### Appendix  
#### Example direct API call using the SDK:  
 ```python
 def listAllUsers(client):
    url = '{0}/users'.format(API.BASE_API_URL)
    box_response = client.make_request('GET', url)
    response = box_response.json()
    return [User(client._session, item['id'], item) for item in response['entries']]
```  

#### Box SDK can be found at:  
https://github.com/box/box-python-sdk  


### Screenshots  
Home Page (List View):  
![List View](https://raw.githubusercontent.com/dann815/boxflaskjwt/6edfaf250c7842f592a10d271a5cfba2d07d614f/Listview.png?raw=true “List View”)   
User Page (Detail View):  
![Detail View](https://raw.githubusercontent.com/dann815/boxflaskjwt/6edfaf250c7842f592a10d271a5cfba2d07d614f/Detailview.png?raw=true “Detail View”)  


#### Flask Quickstart:  
<http://flask.pocoo.org/docs/0.10/quickstart/>  


Contact: DanK@box.com  
