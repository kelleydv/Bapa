from bapa import app
import requests, json

def verify_recaptcha(response):

    data = {
        'secret': app.config['RECAPTCHA_SECRET'],
        'response': response
    }

    resp = requests.post(app.config['RECAPTCHA_ENDPOINT'], data=data)

    if json.loads(resp.text)['success'] == True:
        return True
