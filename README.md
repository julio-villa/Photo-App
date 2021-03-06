## Interacting with the app
The user data in this app is generated randomly. For testing and interacting with the app, use the username: 'username' and the password: 'password'.

## Installation
To install dependencies, navigate to your `photo-app` directory on your command line and issue the following commands:

```shell
pip3 install -r requirements.txt
# If the above command doesn't work, try one of the commands below:
# py -m pip install -r requirements.txt
# python3 -m pip install -r requirements.txt
# python -m pip install -r requirements.txt
```
Depending on your python interpreter/environment, you might have to install some of the packages using a different package management system.
Ex. "conda install psycopg2" etc.

## Running your Flask Server

### On Mac / Linux
```shell
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### On Windows
```shell
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
# alternative commands to try if "flask run" doesn't work:
# py -m flask run
# python3 -m flask run
# python -m flask run
```