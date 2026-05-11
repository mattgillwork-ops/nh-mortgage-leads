import React, { useEffect, useState } from 'react';

function TaskHistory() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/task_history')
      .then(response => response.json())
      .then(data => setTasks(data.tasks));
  }, []);

  return (
    <div>
      <h2>Task History</h2>
      <ul>
        {tasks.map(task => (
          <li key={task.id}>{task.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default TaskHistory;
