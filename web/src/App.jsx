import React, { useEffect, useState } from 'react';
import './App.css';

const App = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const eventSource = new EventSource('http://127.0.0.1:5007/meta-stream'); // Connect to the backend for streaming data

    eventSource.onmessage = function(event) {
      const newData = JSON.parse(event.data);
      setData(newData); // Update state with the incoming data
    };

    eventSource.onerror = function(error) {
      console.log('Error while receiving data: ', error);
    };

    return () => {
      eventSource.close(); // Clean up when the component unmounts
    };
  }, []);

  return (
    <div className="App">
      <h1>LineAlert Dashboard</h1>
      <h2>Real-time Data</h2>
      {data ? (
        <pre>{JSON.stringify(data, null, 2)}</pre>  // Display the received data
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;
