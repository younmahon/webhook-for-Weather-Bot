import json
import os
import requests
import urllib.request




from flask import Flask

from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))

    res = makeResponse(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r




def makeResponse(req):
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    api_key = 'AIzaSyCGJtTMyQuLDacLAQNJjd3AeNAnRgLnB_A'
    result = req.get("queryResult")
    parameters = result.get("parameters")
    size = parameters.get("size")
    DoenerType = parameters.get("DoenerType")
    Fleisch = parameters.get("Fleisch")
    Toppings = parameters.get("Toppings")
    Scharf = parameters.get("Scharf")
    Sauce = parameters.get("Sauce")
    address = parameters.get("address")
    destination = parameters.get("destination")
    origin = "Mozartstrasse+16+Heppenheim"
    destination = address.replace('','+')
    nav_request = 'origin={}&destination={}&key={}'.format(origin,destination,api_key)
    request = endpoint + nav_request
    response = urllib.request.urlopen(request).read()
    directions = json.loads(response)
    duration = directions['routes'][0]['legs'][0]['duration']['text']
    speech = "wunderbar, Sie haben folgendes bestellt:"+size +DoenerType+ " mit" +Fleisch+", Sie wollen es "+Toppings+", also "+Sauce+" und "+Scharf+". Wir liefern zur Addresse: "+address+". Die Lieferung Dauer ist: "+duration+
    ". Bleiben Sie gesund, kommen Sie morgen bitte !"

    ##city = parameters.get("geo-city")
    ##name123 = parameters.get("given-name")
    ##r=requests.get('http://api.apixu.com/v1/current.json?key=a357348be936488c820132836192703%20&q='+city)
    #txt=requests.get('https://quota.glitch.me/random')
    #json_object1 = txt.json()
    #text1= json_object1.get("quoteText")
    json_object = r.json()
    ##weather=json_object.get("current")
    ##temperature=weather.get("temp_c")
    ##strtemperature=str(int(temperature))
    # speech = "Listen " + name123 + ", The forecast for "+city+" is "+strtemperature+" degrees. Remember this quote for today : "+text1
    ##speech = "The forecast now for "+city +" is "+strtemperature+" degrees. "
    return{
  "fulfillmentText": speech,


  "fulfillmentMessages": [
    {
      "text": {
        "text": [speech]
      }
    }
  ],
  "source": "<Text response>"
}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
