import requests
from requests import get
import ipinfo
import json
from flask import Flask, request, jsonify
import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

#  API service
app = Flask(__name__)
app.debug = True


def checkCurrentWeather():
    api_endpoint = "http://ipinfo.io"
    api_key = "57b4c02b4891c3"
    auth = requests.auth.HTTPBasicAuth(api_key, "")
    response = requests.get(api_endpoint, auth=auth)

    location = response.json()
    city = location.get("city")
    country = location.get("country")

    responseWeather = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?units=metric&q=' + city + ',' + country + '&appid=c766a39d9c387c7527524122df20c77f').text
    weather = json.loads(responseWeather)

    temperature = weather['main']['temp']

    # format response as json
    value = {"city": city, "country": country, "degrees ": temperature}
    json_value = json.dumps(value)

    return json_value


def WeatherByCity(req_city):
    city = req_city
    country = "IL"

    weatherReq = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?units=metric&q=' + city + ',' + country + '&appid=c766a39d9c387c7527524122df20c77f').text

    weather = json.loads(weatherReq)
    degrees = weather['main']['temp']

    value = {"city": city, "country": country, "degrees": degrees}
    json_value = json.dumps(value)

    return json_value


def getDriveStatus(status_filter):
    with open("input.json", "r") as myfile:
        data = json.load(myfile)
        json_formatted = json.dumps(data)
    return json_formatted


@app.route('/v1/api/checkCurrentWeather', methods=['GET'])
def request_weather_by_ip():
    return checkCurrentWeather()


@app.route('/v1/api/checkCityWeather', methods=['GET'])
def request_weather_by_city():
    req_city = str(request.args.get('city'))  # ?city=Haifa
    return WeatherByCity(req_city)


@app.route('/v1/api/driveStatus', methods=['POST'])
def update_drive_status():
    try:
        with open('input.json', 'r') as outfile:
            data = json.load(outfile)
            status = 'success'
    except Exception as e:
        logging.error("an error occurred writing the file", e)
        status = 'failure'
    status_message = {
        "message": status
    }
    return json.dumps(status_message)


@app.route('/v1/api/driveStatus', methods=['GET'])
def request_status():
    statusFilter = str(request.args.get('status'))
    return getDriveStatus(statusFilter)


@app.route('/', methods=['GET'])
def home():
    return "hello, welcome to the outRain ex, please send proper endpoint"


if __name__ == '__main__':
    app.run(debug=True, port=7777, host='0.0.0.0')
    app.logger.info("status filter %s", request.args.get('status'))
