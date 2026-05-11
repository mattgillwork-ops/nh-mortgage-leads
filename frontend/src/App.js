```javascript
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws');

    socket.onopen = () => {
      console.log('Connected to WebSocket server');
    };

    socket.onmessage = (event) => {
      setLogs((prevLogs) => [...prevLogs, event.data]);
    };

    socket.onclose = () => {
      console.log('Disconnected from WebSocket server');
    };

    
return (
  <div className="App">
    <h1>Live Logs</h1>
    <ul>
      {logs.map((log, index) => (
        <li key={index}>{log}</li>
      ))}
    </ul>
    <h2>RAG Memory Graph</h2>
    <p>Placeholder for RAG memory graph</p>
    <h2>Agent Status</h2>
    <p>Placeholder for agent status</p>
  </div>
);
) => {
      socket.close();
    };
  }, []);

  
return (
  <div className="App">
    <h1>Live Logs</h1>
    <ul>
      {logs.map((log, index) => (
        <li key={index}>{log}</li>
      ))}
    </ul>
    <h2>RAG Memory Graph</h2>
    <p>Placeholder for RAG memory graph</p>
    <h2>Agent Status</h2>
    <p>Placeholder for agent status</p>
  </div>
);

    <div className="App">
      <h1>Live Logs</h1>
      <ul>
        {logs.map((log, index) => (
          <li key={index}>{log}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
```
