import React, { useState, useEffect } from "react";
import AlertComponent from "./AlertComponent";

const Dashboard = () => {
  const [alerts, setAlerts] = useState([]);
  const [driftData, setDriftData] = useState([]);

  // Fetch alerts and drift data every 5 seconds
  useEffect(() => {
    const fetchData = async () => {
      try {
        const alertsResponse = await fetch("http://localhost:5007/alert");
        const driftDataResponse = await fetch("http://localhost:5007/drift");

        if (!alertsResponse.ok || !driftDataResponse.ok) {
          throw new Error("Failed to fetch data");
        }

        const alertsData = await alertsResponse.json();
        const driftData = await driftDataResponse.json();

        setAlerts(alertsData);
        setDriftData(driftData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 5000); // Fetch data every 5 seconds

    return () => clearInterval(intervalId); // Cleanup the interval on component unmount
  }, []);

  return (
    <div>
      <h1>LineAlert Dashboard</h1>
      <h2>Alerts</h2>
      {alerts.length === 0 ? (
        <p>No alerts available.</p>
      ) : (
        alerts.map((alert, index) => (
          <AlertComponent key={index} alert={alert} />
        ))
      )}
      <h2>Drift Data</h2>
      <ul>
        {driftData.map((data, index) => (
          <li key={index}>
            {data.tag}: {data.value} | Severity: {data.severity} | Change:{" "}
            {data.change}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
