import React, { useState, useEffect } from 'react';

const AlertComponent = () => {
    const [alert, setAlert] = useState(null);

    useEffect(() => {
        // Polling the Flask backend for alerts
        const fetchAlerts = () => {
            fetch("http://localhost:5007/alert")
                .then(res => res.json())
                .then(data => {
                    setAlert(data);  // Update alert state
                });
        };

        const interval = setInterval(fetchAlerts, 5000);  // Poll every 5 seconds
        return () => clearInterval(interval);  // Clean up on unmount
    }, []);

    if (!alert) return <div>Loading...</div>;

    return (
        <div className={`alert alert-${alert.severity.toLowerCase()}`}>
            <p>{alert.message}</p>
            <p>{alert.timestamp}</p>
        </div>
    );
};

export default AlertComponent;
