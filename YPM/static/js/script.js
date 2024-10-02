document.getElementById('single-prediction-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const data = {
        Area: document.getElementById('area').value,
        Item: document.getElementById('item').value,
        average_rain_fall_mm_per_year: parseFloat(document.getElementById('rainfall').value),
        avg_temp: parseFloat(document.getElementById('temperature').value)
    };

    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('prediction-result').innerText = `Predicted Yield: ${data.prediction}`;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
