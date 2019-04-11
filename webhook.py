import json
import os
import requests
import google



from flask import Flask
from google.cloud.translate import translate
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
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    name123 = parameters.get("given-name")
    r=requests.get('http://api.apixu.com/v1/current.json?key=a357348be936488c820132836192703%20&q='+city)
    json_object = r.json()
    weather=json_object.get("current")
    temperature=weather.get("temp_c")
    strtemperature=str(int(temperature))
    speech = "Listen " + name123 + ", The forecast for "+city+" is "+strtemperature+" degrees"
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
