# Box App Users - Python/Flask Quickstart
Code is commented. Everything important is in /main.py  

Set up a Box Developer Application at:  
<https://box-content.readme.io/v2.0/docs/box-platform>  



### Step 0: Pull code  
Navigate to the folder you want to place /boxflaskjwt/
```
cd ~/dev 
git clone https://github.com/dann815/boxflaskjwt.git  
```

### Step 1: Install packages   
It's always recommended to use [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) with Python  
Use python 2.7.*  **Note: Does not work with 3.x**  

1.1 Create and setup a virtualenv with something like this:
Note**: Folder "pythonruntime" will be a created
```
sudo pip install virtualenv
virtualenv pythonruntime && source pythonruntime/bin/activate && pip install -U setuptools wheel && pip install -U pip && pip install -U boxsdk[jwt]
```
 
1.2 Any time you want to use the virtualenv again in a new terminal window:
```
source pythonruntime/bin/activate
```


### Step 2: Generate your RSA keys  
2.1 Create a private key…  
...with a password:  
```
openssl genrsa -aes256 -out rsakey.pem 2048
```  
.. or without a password:  
```
openssl genrsa -out rsakey.pem 2048 
```  


2.2 Create a public key from the private key:  
```
openssl rsa -pubout -in rsakey.pem -out rsapublic.pem  
```

### Step 3: Input your RSA keys  
3.1 Copy your public key:  
```
cat rsapublic.pem | pbcopy  
```
3.2 Add the public key to your app at <https://developers.box.com/>->My Apps  
Follow the instructions at: <https://box-content.readme.io/v2.0/docs/app-auth>  
Put the private key in your project folder at the root level.  

### Step 4: Configuration  
4.1 Create a file named settings.cfg   
4.2 Add the following lines to settings.cfg:  
```
# General config
DEBUG = True
SECRET_KEY = 'A RANDOM SECRET KEY'

# Box config
CLIENT_ID = 'YOUR CLIENT ID'
CLIENT_SECRET = 'YOUR CLIENT SECRET'
EID = 'YOUR EID'
``` 
Note: Generate a random string for the SECRET_KEY by running: 
```
python
import os
os.urandom(24)
```  
  
3.3 Set an environment variable to point to the location of the settings.cfg file  
```
export BOX_APPLICATION_SETTINGS=/Users/danielkaplan/dev/jwtFlask/settings.cfg
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
