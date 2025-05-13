// web_dashboard.js

// Function to fetch alerts from the backend
async function fetchAlerts() {
    try {
        // Make a POST request to the backend server for a test alert (This is just for testing)
        const res = await fetch('http://192.168.0.16:5007/alert', {
            method: 'POST',
            body: JSON.stringify({
                message: 'Test alert',
                severity: 'GREEN',
                timestamp: new Date().toISOString(),
            }),
            headers: {
                'Content-Type': 'application/json',
            },
        });

        // Parse the response from the backend
        const data = await res.json();
        if (data.status === 'success') {
            // Update the UI with the received alert
            const alertMessage = data.message;
            const severity = data.severity;  // Dynamically set severity based on response
            const alertContainer = document.getElementById('alerts-container');
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert ${severity.toLowerCase()}`;
            alertDiv.innerHTML = `<strong>${severity}</strong>: ${alertMessage}`;
            alertContainer.appendChild(alertDiv);
        }
    } catch (error) {
        console.error('Error fetching alert:', error);
    }
}

// Call the fetchAlerts function every 5 seconds
setInterval(fetchAlerts, 5000);

// Initialize fetching alerts when the page loads
window.onload = fetchAlerts;
