import React, { useEffect, useState } from 'react';

function MemoryRAGData() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/memory_rag_data')
      .then(response => response.json())
      .then(data => setData(data.data));
  }, []);

  return (
    <div>
      <h2>Memory RAG Data</h2>
      <ul>
        {data.map(item => (
          <li key={item.id}>{item.content}</li>
        ))}
      </ul>
    </div>
  );
}

export default MemoryRAGData;
