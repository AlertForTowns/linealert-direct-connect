// Function to send alert data to Flask backend
function sendAlertToBackend(alertData) {
    fetch('http://localhost:5007/alert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(alertData),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Alert received:', data);
        updateFrontend(data);  // Update the frontend with the received alert
    })
    .catch((error) => {
        console.error('Error sending alert:', error);
    });
}

// Example function to handle drift detection
function handleDrift(previousValue, currentValue) {
    const drift = currentValue - previousValue;
    const severity = drift > 2 ? 'YELLOW' : 'GREEN';  // Adjust threshold for severity

    const alertData = {
        message: `Drift detected! Previous value: ${previousValue}, Current value: ${currentValue}`,
        severity: severity,
        timestamp: new Date().toISOString(),
    };

    sendAlertToBackend(alertData);  // Send drift alert to the backend
}

// Call handleDrift periodically or based on drift detection
handleDrift(50, 55);  // Example drift detection
