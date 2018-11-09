# Simple-Freeradius-Admin
A fast and intuitive internet user administrator.

## How to

The recommended way to set this up is to use https://github.com/Karlheinzniebuhr/Radius-Stack


Otherwise run
```
git clone https://github.com/Karlheinzniebuhr/Simple-Freeradius-Admin/
cd Simple-Freeradius-Admin
```
configure your DB in keys.py and __init__.py

```
docker build --tag radadmin .
docker run --name radadmin -p 5000:5000/tcp radadmin
```

### Or

- Go ahead and setup Freeradius with MySql. [Documentation](https://wiki.freeradius.org/guide/sql-howto)
```
git clone https://github.com/Karlheinzniebuhr/Simple-Freeradius-Admin/
cd Simple-Freeradius-Admin
pip install -r requirements.txt
```
- Configure keys.py with your freeradius mysql credentials
- Run the server
```
flask run
```
