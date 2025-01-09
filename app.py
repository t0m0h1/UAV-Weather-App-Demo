

import json
from flask import Flask, jsonify, request, render_template
import requests

# Load API key from config.json
def load_api_key():
    with open('keys.json') as config_file:
        config = json.load(config_file)
    return config['API_KEY']

app = Flask(__name__)

API_KEY = load_api_key()  # Load the API key
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    location = request.args.get('location', default='New York')

    if not location.isalpha():  # Validate the location input
        return jsonify({'error': 'Invalid location'}), 400

    params = {'q': location, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch weather data', 'details': response.json().get('message', 'Unknown error')}), response.status_code

    data = response.json()

    weather_info = {
        'temperature': data['main']['temp'],
        'wind_speed': data['wind']['speed'],
        'visibility': data.get('visibility', 10000),
        'conditions': data['weather'][0]['description'],
        'icon_url': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
    }

    if weather_info['wind_speed'] > 10 or weather_info['visibility'] < 5000 or weather_info['temperature'] < 0:
        weather_info['flyable'] = False
        weather_info['reason'] = 'High wind speed, low visibility, or freezing temperature'
    else:
        weather_info['flyable'] = True

    return jsonify(weather_info)

if __name__ == '__main__':
    app.run(debug=True)
