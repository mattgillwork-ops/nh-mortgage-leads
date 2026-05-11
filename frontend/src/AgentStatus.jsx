import React, { useEffect, useState } from 'react';

function AgentStatus() {
  const [status, setStatus] = useState('inactive');

  useEffect(() => {
    fetch('http://localhost:5000/api/agent_status')
      .then(response => response.json())
      .then(data => setStatus(data.status));
  }, []);

  return (
    <div>
      <h2>Agent Status</h2>
      <p>{status}</p>
    </div>
  );
}

export default AgentStatus;
