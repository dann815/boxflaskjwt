# boxflaskjwt
Read the comments in the code.  They will help :)  
Everything important is at /main.py  

Follow instructions to set up a Box Developer Application:  
<https://box-content.readme.io/v2.0/docs/box-platform>  



### Step 0: Pull code  
```
git clone https://github.com/dann815/boxflaskjwt.git  
```

### Step 1: Install packages   
Recommended: [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)  
Use python 2.7.*  **Note: Does not work with 3.x**  
```
pip install Flask   
pip install boxsdk    
pip install boxsdk[jwt]  
```

### Step 2: Generate your RSA keys  
Create a private key  
without password:  
```
openssl genrsa -out rsakey.pem 2048 
```  
OR with password:  
```
openssl genrsa -aes256 -out rsakey.pem 2048
```  

Then create a public key from the private key:  
```
openssl rsa -pubout -in rsakey.pem -out rsapublic.pem  
```

### Step 3: Input your RSA keys  
Copy your public key:  
```
cat rsapublic.pem | pbcopy  
```
Add the public key to your app at <https://developers.box.com/>->My Apps  
Put the private key in your project folder at /box/rsakey.pem  

### Step 4: Set environment variables  
On Mac: Open ~/.bash_profile in a text editor and add the following lines (with your values from developers.box.com)  
```
export BOX_SDK_CLIENTID=1234567890ABCD  
export BOX_SDK_CLIENTSECRET=ABCDEFGHI1234  
export BOX_SDK_EID=123456  
```

### Step 5: Run the code  
```
python main.py  
```
Navigate to:  
<http://localhost:5000> 


  
Contact: DanK@box.com  
  
  
  
#### Box SDK can be found at:  
https://github.com/box/box-python-sdk  

#### Flask Quickstart:  
<http://flask.pocoo.org/docs/0.10/quickstart/>  

#### Example custom API call using the SDK's client object:  
 ```python
 def listAllUsers(client):
    url = '{0}/users'.format(API.BASE_API_URL)
    box_response = client.make_request('GET', url)
    response = box_response.json()
    return [User(client._session, item['id'], item) for item in response['entries']]
```
