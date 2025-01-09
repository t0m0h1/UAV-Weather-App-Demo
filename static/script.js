async function fetchWeather() {
    const location = document.getElementById('location').value.trim();
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = ""; // Clear previous results

    // Check if location is provided
    if (!location) {
        resultDiv.innerHTML = `<p class="error-message">Please enter a location.</p>`;
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/weather?location=${location}`);
        if (!response.ok) {
            throw new Error('Failed to fetch weather data');
        }
        const data = await response.json();

        // Display weather information
        resultDiv.innerHTML = `
            <div class="weather-card">
                <h3 class="location-title">Weather in ${location}</h3>
                <img src="${data.icon_url}" alt="Weather icon" class="weather-icon">
                <p class="weather-detail"><strong>Temperature:</strong> ${data.temperature}°C</p>
                <p class="weather-detail"><strong>Wind Speed:</strong> ${data.wind_speed} m/s</p>
                <p class="weather-detail"><strong>Visibility:</strong> ${data.visibility} meters</p>
                <p class="weather-detail"><strong>Conditions:</strong> ${data.conditions}</p>
                <p class="weather-detail"><strong>Flyable:</strong> ${data.flyable ? 'Yes' : 'No'}</p>
                ${!data.flyable ? `<p class="weather-detail"><strong>Reason:</strong> ${data.reason}</p>` : ''}
            </div>
        `;
    } catch (error) {
        console.error(error);
        // Handle error and display message
        resultDiv.innerHTML = `<p class="error-message">Error: ${error.message}</p>`;
    }
}
