async function fetchWeather() {
    const location = document.getElementById('location').value;
    const response = await fetch(`http://127.0.0.1:5000/weather?location=${location}`);
    const data = await response.json();

    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `
        <h3>Weather in ${location}</h3>
        <p>Temperature: ${data.temperature}°C</p>
        <p>Wind Speed: ${data.wind_speed} m/s</p>
        <p>Visibility: ${data.visibility} meters</p>
        <p>Conditions: ${data.conditions}</p>
        <p>Flyable: ${data.flyable ? 'Yes' : 'No'}</p>
        ${!data.flyable ? `<p>Reason: ${data.reason}</p>` : ''}
    `;
}
