from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Weather API Configuration
API_KEY = 'your_openweather_api_key'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

@app.route('/weather', methods=['GET'])
def get_weather():
    # Get location from query parameters
    location = request.args.get('location', default='New York')
    
    # Fetch weather data
    params = {'q': location, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    # Extract drone-relevant data
    weather_info = {
        'temperature': data['main']['temp'],
        'wind_speed': data['wind']['speed'],
        'visibility': data['visibility'],
        'conditions': data['weather'][0]['description'],
    }
    
    # Add fly/no-fly decision logic
    if weather_info['wind_speed'] > 10:  # Example: limit wind speed to 10 m/s
        weather_info['flyable'] = False
        weather_info['reason'] = 'High wind speed'
    else:
        weather_info['flyable'] = True
    
    return jsonify(weather_info)

if __name__ == '__main__':
    app.run(debug=True)
