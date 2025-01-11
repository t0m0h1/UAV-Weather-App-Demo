import json
from flask import Flask, jsonify, request, render_template
import requests

# Load API key from keys.json
def load_api_key(file_path='keys.json'):
    try:
        with open(file_path) as config_file:
            config = json.load(config_file)
        return config.get('API_KEY')
    except (FileNotFoundError, KeyError) as e:
        raise RuntimeError(f"Failed to load API key: {e}")

app = Flask(__name__)

try:
    API_KEY = load_api_key()  # Load the API key
except RuntimeError as e:
    print(e)
    API_KEY = None

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    location = request.args.get('location', default='New York')

    # Validate the location input
    if not location.isalpha():
        return jsonify({'error': 'Invalid location. Only alphabetic characters are allowed.'}), 400

    if not API_KEY:
        return jsonify({'error': 'API key not available. Please check your configuration.'}), 500

    params = {'q': location, 'appid': API_KEY, 'units': 'metric'}

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to fetch weather data', 'details': str(e)}), 500

    data = response.json()

    weather_info = {
        'temperature': data['main']['temp'],
        'wind_speed': data['wind']['speed'],
        'visibility': data.get('visibility', 10000),
        'conditions': data['weather'][0]['description'],
        'icon_url': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
    }

    # Determine flyability
    if weather_info['wind_speed'] > 10:
        weather_info.update({'flyable': False, 'reason': 'High wind speed'})
    elif 'snow' in weather_info['conditions'].lower():
        weather_info.update({'flyable': False, 'reason': 'Snow forecast in this area'})
    elif weather_info['visibility'] < 5000:
        weather_info.update({'flyable': False, 'reason': 'Low visibility'})
    elif weather_info['temperature'] < 0:
        weather_info.update({'flyable': False, 'reason': 'Freezing temperature'})
    else:
        weather_info.update({'flyable': True, 'reason': 'Weather conditions are suitable for flying'})

    return jsonify(weather_info)

# Driver code
if __name__ == '__main__':
    app.run(debug=True)

