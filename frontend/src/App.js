import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

function App() {
  const [driftData, setDriftData] = useState([]);
  const [filter, setFilter] = useState('All');

  // Fetch data function
  const fetchData = useCallback(async () => {
    try {
      const driftResponse = await axios.get('http://localhost:5007/drift');
      console.log('Fetched Drift Data:', driftResponse.data);  // Debugging log
      setDriftData(driftResponse.data);
    } catch (error) {
      console.error('Error fetching data: ', error);
    }
  }, []);

  useEffect(() => {
    fetchData();
    const interval = setInterval(() => {
      fetchData();
    }, 5000); // Refresh every 5 seconds

    return () => clearInterval(interval);  // Clean up interval
  }, [fetchData]);

  // Filter data based on severity
  const filteredData = driftData.filter((data) => {
    if (filter === 'All') return true;
    return data.severity === filter;
  });

  return (
    <div className="App">
      <h1>LineAlert Dashboard</h1>

      {/* Filter Options */}
      <div>
        <button onClick={() => setFilter('All')}>All Data</button>
        <button onClick={() => setFilter('Low')}>Low Severity</button>
        <button onClick={() => setFilter('Moderate')}>Moderate Severity</button>
        <button onClick={() => setFilter('Bad')}>Bad Severity</button>
      </div>

      {/* Drift Data Display */}
      <div>
        <h2>Drift Data</h2>
        {filteredData.length > 0 ? (
          filteredData.map((data, index) => (
            <div key={index}>
              <p>Tag: {data.tag}</p>
              <p>Value: {data.value}</p>
              <p>Severity: {data.severity}</p>
              <p>Change: {data.change}%</p>
              <p>Timestamp: {data.timestamp || 'No Timestamp Available'}</p>
              <hr />
            </div>
          ))
        ) : (
          <p>No Drift Data Available</p>
        )}
      </div>
    </div>
  );
}

export default App;
