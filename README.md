# BAPA

Website for the Bay Area Paragliding Association (Work In Progress)

### Requirements
- [node/npm](https://nodejs.org/) (for front-end dependencies)
- [Python 3](https://www.python.org/)
[Dyno Metadata](https://devcenter.heroku.com/articles/dyno-metadata)
```bash
heroku labs:enable runtime-dyno-metadata -a <app name>
```
This allows the app to know the commit hash when using
github integrations.

----
### Run Locally
```
$ cd Bapa
$ pip3 install -r requirements.txt #python dependencies
$ npm install #front-end dependencies
$ export ENV=DEV
$ python3 server.py
 * Running on http://0.0.0.0:5000/
```

----
### More on Front-End
To install dependencies, run `$ npm install`, or just `$ bower install` if you already have bower installed.  See [bower.json](./bower.json) for a list of front-end components.

----
### Testing
```
export ENV=TEST
python3 test.py
```

----
### Environment Variables
reCaptcha, Paypal, and cloudinary environment variables need to be set for full
functionality.

###### `ENV` (required)
  - `DEV`, `TEST`, or `PROD`
  - Used to load the appropriate configuration from [config.py](https://github.com/kelleydv/Bapa/blob/develop/bapa/config.py)

###### `SECRET_KEY`
  - For encrypting session data. Use something cryptographically secure. Changing this will force logout.

###### `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER`
  - Credentials for SMTP server
  - See [Flask-Mail](https://pythonhosted.org/Flask-Mail/#configuring-flask-mail) documentation.

###### `USHPA_CHAPTER`, `USHPA_PIN`
  - Credentials for the USHPA API
  - Used to retrieve pilot ratings, etc.
  - See usage [in services](https://github.com/kelleydv/Bapa/blob/develop/bapa/services/ushpa.py).

###### `RECAPTCHA_SECRET`, `RECAPTCHA_SITEKEY`
  - See [reCaptcha](https://developers.google.com/recaptcha/intro) documentation.
  - See usage [in services](https://github.com/kelleydv/Bapa/blob/develop/bapa/services/recaptcha.py).
  - The site key is used for displaying widgets

----
### Contributing
Pull requests are always welcome, as are issues.  Check the issues if you are looking for something to help out with.
