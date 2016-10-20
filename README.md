# BAPA

Website for the Bay Area Paragliding Association (Work In Progress)

### Requirements
- [node/npm](https://nodejs.org/) (for front-end dependencies)
- [Python 3](https://www.python.org/)

### Run Locally
```
$ cd Bapa
$ pip3 install -r requirements.txt #python dependencies
$ npm install #front-end dependencies
$ export env=dev
$ python3 server.py
 * Running on http://0.0.0.0:5000/
```

### Front-End
To install dependencies, run `$ npm install`, or just `$ bower install` if you already have bower installed.  See [bower.json](./bower.json) for a list of front-end components.

### Testing
```
export env=test
python3 test.py
```

### Contributing
Pull requests are always welcome, as are issues.  Check the issues if you are looking for something to help out with.
