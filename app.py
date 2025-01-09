from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

# Weather API Configuration
API_KEY = 'dbb1f03d6f0d9651b3d9ffd9b82caea6'  # Retain hardcoded API key
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/weather', methods=['GET'])
def get_weather():
    # Get location from query parameters
    location = request.args.get('location', default='New York')
    
    # Fetch weather data
    params = {'q': location, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        data = response.json()
        return jsonify({'error': 'Failed to fetch weather data', 'details': data.get('message', 'Unknown error')}), 400
    
    data = response.json()
    
    # Extract drone-relevant data
    weather_info = {
        'temperature': data['main']['temp'],
        'wind_speed': data['wind']['speed'],
        'visibility': data.get('visibility', 10000),  # Default visibility to 10,000 meters if missing
        'conditions': data['weather'][0]['description'],
    }
    
    # Add fly/no-fly decision logic
    if weather_info['wind_speed'] > 10 or weather_info['visibility'] < 5000 or weather_info['temperature'] < 0:
        weather_info['flyable'] = False
        weather_info['reason'] = 'High wind speed, low visibility, or freezing temperature'
    else:
        weather_info['flyable'] = True
    
    
    return jsonify(weather_info)


if __name__ == '__main__':
    app.run(debug=True)
