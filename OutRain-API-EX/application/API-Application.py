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
        lines = myfile.readlines()
        statusCount = (' '.join(lines)).count(status_filter)
        result = ""
        for eachDrive in lines:
            if eachDrive.find(status_filter) > 0:
                print(eachDrive)
                result += eachDrive
        return "found " + str(statusCount) + " " + status_filter + " drives\n" + result


@app.route('/v1/api/checkCurrentWeather', methods=['GET'])
def request_weather_by_ip():
    return checkCurrentWeather()


@app.route('/v1/api/checkCityWeather', methods=['GET'])
def request_weather_by_city():
    req_city = str(request.args.get('city'))  # ?city=Haifa
    return WeatherByCity(req_city)


@app.route('/v1/api/driveStatus', methods=['POST'])
def update_drive_status():
    receivedJson = request.get_json()
    status = 'success'
    try:
        with open('input.json', 'w') as outfile:
            outfile.write(receivedJson)
    except Exception as e:
        logging.error("an error occurred writing the file", e)
        status = 'failure'
    statusMessage = {
        "message": status
    }
    return json.dumps(statusMessage)


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
