import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';

// You can use createRoot for React 18+
// ReactDOM.createRoot(document.getElementById('root')).render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>
// );

const root = document.getElementById('root');
ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  root
);
