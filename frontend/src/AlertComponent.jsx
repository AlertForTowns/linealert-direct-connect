import React, { useState, useEffect } from 'react';

// Alert component to display individual alert details
const AlertComponent = ({ alert }) => {
  const [isDetailsVisible, setIsDetailsVisible] = useState(false);
  const [alertDetails, setAlertDetails] = useState(null);

  // Toggle the visibility of the details for the alert
  const handleDetailsClick = async (alertId) => {
    const response = await fetch(`/alert/${alertId}`);
    const data = await response.json();
    setAlertDetails(data);
    setIsDetailsVisible(!isDetailsVisible);
  };

  // Function to get the appropriate class based on severity
  const getAlertClass = (severity) => {
    switch (severity) {
      case 'Low':
        return 'alert Low';
      case 'Moderate':
        return 'alert Moderate';
      case 'Bad':
        return 'alert Bad';
      case 'Critical':
        return 'alert Critical';
      default:
        return 'alert';
    }
  };

  return (
    <div className={getAlertClass(alert.severity)}>
      <p>{alert.severity}: {alert.value}</p>
      <button onClick={() => handleDetailsClick(alert.id)}>Show Details</button>
      {isDetailsVisible && alertDetails && (
        <div className="alert-details">
          <p>{alertDetails.description}</p>
          <p>Suggested Fix: {alertDetails.suggestedFix}</p>
        </div>
      )}
    </div>
  );
};

export default AlertComponent;
