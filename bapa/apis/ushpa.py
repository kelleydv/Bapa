from bapa import app
import requests

def get_pilot_data(ushpa):
    """Access the USHPA API and return a dictionary of data"""
    req = app.config['USHPA_HOST']
    req += 'ushpa_validation_ratings.asp?chapter=%s&pin=%s&ushpa=%s' 
    data = requests.get( req % (app.config['USHPA_CHAPTER'], app.config['USHPA_PIN'], ushpa) )
    #Parse plain text
    data = ( x for x in data.text.strip().split('\n') )
    data = ( x.split(':') for x in data )
    data = { k:v.strip() for k,v in data }
    return data
