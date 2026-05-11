import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

function App() {
  const [taskHistory, setTaskHistory] = useState([]);
  const [agentStatus, setAgentStatus] = useState('');
  const [memoryRagData, setMemoryRagData] = useState([]);

  useEffect(() => {
    socket.on('task-history', (data) => {
      setTaskHistory(data.tasks);
    });

    socket.on('agent-status', (data) => {
      setAgentStatus(data.status);
    });

    socket.on('memory-rag', (data) => {
      setMemoryRagData(data.data);
    });
  }, []);

  return (
    <div>
      <h1>Task History</h1>
      <ul>
        {taskHistory.map((task, index) => (
          <li key={index}>{task}</li>
        ))}
      </ul>

      <h1>Agent Status</h1>
      <p>{agentStatus}</p>

      <h1>Memory RAG Data</h1>
      <ul>
        {memoryRagData.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
