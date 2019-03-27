import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response
import plivo

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
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    r=requests.get('http://api.apixu.com/v1/current.json?key=a357348be936488c820132836192703%20&q='+city+)
    json_object = r.json()
    weather=json_object.get("current")
    temperature=weather.get("temp_c")
    speech = "The forecast for"+city+" is "+temperature
    return {
    "speech": speech,
    "displayText": speech,
    "source": "apiai-weather-webhook"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
