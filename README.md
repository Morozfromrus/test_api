# test_api

## How to install:
1. clone repository - `git clone https://github.com/Morozfromrus/test_api`
2. use virtualenv - `virtualenv -p python3 <VNAME>; source <VNAME>/bin/activate`
3. install requirements - `cd <CLONE_DIR>/test_api; pip install -r requirements.txt`
4. make .env file - `nano <CLONE_DIR>/test_api/test_api/.env`
```
DATABASE_URL=sqlite:///db.sqlite3
SECRET_KEY=<TOP_SECRET_KEY>
DEBUG=True
```
*for easy config example* - `touch <CLONE_DIR>/test_api/db.sqlite3`

5. migrate database - `cd <CLONE_DIR>/test_api/; python manage.py migrate`
6. run tests - `cd <CLONE_DIR>/test_api/; python manage.py test`
7. run test or deploy - `cd <CLONE_DIR>/test_api/; python manage.py runserver`

Enjoy

*P.S. I forgot change ALLOWED_HOSTS*
