// src/components/DataStream.jsx

import React, { useEffect, useState } from 'react';

const DataStream = () => {
  const [streamData, setStreamData] = useState(null);

  useEffect(() => {
    // Create a new EventSource to listen for data
    const eventSource = new EventSource('http://127.0.0.1:5007/meta-stream');

    // When new data comes in, update the state
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setStreamData(data);
    };

    // If there's an error with the stream, log it
    eventSource.onerror = (error) => {
      console.error('Error with the EventSource:', error);
    };

    // Clean up the event source when the component unmounts
    return () => {
      eventSource.close();
    };
  }, []);

  return (
    <div>
      <h1>Real-time Data</h1>
      <pre>{streamData ? JSON.stringify(streamData, null, 2) : 'Loading...'}</pre>
    </div>
  );
};

export default DataStream;
