from bapa import app
import requests

def verify_ipn(data):
    """Validate a paypal IPN"""
    data = dict(data)
    data['cmd'] = '_notify-validate'
    resp = requests.post(app.config['PAYPAL_ENDPOINT'], data=data)
    if resp.text == 'VERIFIED':
        return True
    return False

#https://developer.paypal.com/docs/classic/ipn/integration-guide/IPNIntro/#protocol_and_arch
