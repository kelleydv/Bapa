# BAPA

Website for the Bay Area Paragliding Association (Work In Progress)

### Requirements
- [postgres](https://www.postgresql.org/)
- [node/npm](https://nodejs.org/) (for front-end dependencies)
- [Python 3](https://www.python.org/)
- [pip3](https://pip.pypa.io/en/latest/installing.html)
- [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) (recommended)

### Set up Python environment (install dependencies via pip)
```
$ cd Bapa
$ virtualenv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

### Install front-end dependencies
run `$ npm install` or just `$ bower install`, if you already have bower installed.  See [bower.json](./bower.json) for a list of front-end components.

### Database Management
TODO: Document this!

### Testing
```
export env=test
python3 test.py
```

### Run locally
```
$ export env=dev
$ source venv/bin/activate
$ python3 server.py
 * Running on http://0.0.0.0:5000/
```

### Contributing
Pull requests are always welcome, as are issues.  Check the issues if you are looking for something to help out with.
