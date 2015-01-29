# BAPA

Website for the Bay Area Paragliding Association

### Requirements
- [mongoDB](http://www.mongodb.org/)
- [Python 3](https://www.python.org/)
- [pip3](https://pip.pypa.io/en/latest/installing.html)
- [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) (recommended)

### Set up Python environment
```
$ cd Bapa
$ virtualenv venv
$ source venv/bin/activate
$ ./provision.sh
```

### Run locally
```
$ ./run_db.sh
$ python3 server.py 
 * Running on http://127.0.0.1:5000/
```
