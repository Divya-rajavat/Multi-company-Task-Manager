import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../Style/Tasks.css'

function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const fetchTasks = async () => {
    try {
      const token = localStorage.getItem('token');
      const tenantDomain = localStorage.getItem('tenant_domain');

      if (!tenantDomain) {
        throw new Error('Tenant domain not found. Please login again.');
      }

      const response = await axios.get(`http://${tenantDomain}:8000/tasks/`, {
        headers: {
          Authorization: `Token ${token}`,
        },
      });

      setTasks(response.data);
    } catch (err) {
      console.error(err);
      setError('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);


  const handleCreate = () => {
    navigate('/create-task');
  }

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="tasks-container">
      <h1>Task List</h1>
      <ul>
        {tasks.map((task) => (
          <li key={task.id} className="task-card">
            <h3>{task.title}</h3>
            <p>{task.description}</p>
            <p>Status: {task.status}</p>
            <p>Assigned To: {task.assigned_to_username}</p>
            {task.due_date && <p>Due Date: {task.due_date}</p>}
          </li>
        ))}
      </ul>
      <button onClick={handleCreate} type="submit" >Create Task</button>
    </div>

  );
}

export default Tasks;
