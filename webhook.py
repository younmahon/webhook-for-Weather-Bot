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
    date = parameters.get("date")
    r=requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=98fe55e4c365cbd0b333744cf7db0f78')
    condition1= "nothing else matters"
    json_object = r.json()
    weather=json_object['list']
    for i in range(0,30):
        if date in weather[i]['dt_txt']:
            condition1= weather[i]['weather'][0]['description']
            break
    condition = condition1
    client = plivo.RestClient()
    response = client.messages.create(
    src='00491728080080',
    dst='00491728080144',
    text='Test Message', )
    print(response)
    speech = "The forecast for"+city+"for "+date+" is "+condition
    return {
    "speech": speech,
    "displayText": speech,
    "source": "apiai-weather-webhook"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
