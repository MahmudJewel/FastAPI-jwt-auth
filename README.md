## FastAPI => JWT authentication and CRUD operarations
# Create has bellow fields
* id ==> primary_key
* email ==> unique
* password ==> any
* is_active ==> boolean 

# Developed API
| SRL | METHOD | ROUTE | FUNCTIONALITY | Required Fields | ACCESS |
| ------- | ------- | ----- | ------------- | ------------- | ------------- |
| *1* | *POST* | ```/token``` | _Login user_| _email, password_| _All users_|
| *2* | *POST* | ```/users/``` | _Create new user_|_email, password_| _All users_|
| *3* | *GET* | ```/users/``` | _Get all users list_|_None_| _All users_|
| *4* | *GET* | ```/users/{user_id}``` | _Get indivisual users details_|_None_| _All users_|
| *5* | *PATCH* | ```/users/{user_id}``` | _Update the user partially	_|_email, password, is_active_| _All users_|
| *6* | *PUT* | ```/users/{user_id}``` | _Full update the user_|_email, password, is_active_| _All users_|
| *7* | *DELETE* | ```/users/{user_id}``` | _Delete the user_|_None_| _All users_|
| *8* | *GET* | ```/``` | _Home page_|_None_| _All users_|


# Tools
### Back-end
#### Language:
	Python (3.11.6)

#### Frameworks:
	FastAPI (0.108.0)
    pydantic (2.5.3)
	
#### Other libraries / tools:
	SQLAlchemy == 2.0.25
    starlette == 0.32.0.post1
    uvicorn == 0.25.0
    python-jose == 3.3.0
	
### Database:
	SQLite

# Setup
The first thing to do is to clone the repository:
```sh
$ https://github.com/MahmudJewel/FastAPI-jwt-auth
```

Create a virtual environment to install dependencies in and activate it:
```sh
$ cd FastAPI-jwt-auth
$ python -m venv venv
$ source venv/bin/activate
```
Then install the dependencies:
```sh
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```sh
(venv)$ uvicorn main:app --reload
```

# Happy Coding
## From ==> Juwel Mahmud

