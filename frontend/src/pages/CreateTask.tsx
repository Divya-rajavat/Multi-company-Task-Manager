import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../Style/CreateTask.css'

const CreateTask = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('todo');
  const [createdBy, setCreatedBy] = useState('');
  const [assignedTo, setAssignedTo] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [users, setUsers] = useState([]);
  const [message, setMessage] = useState('');

  const navigate = useNavigate();

  const tenant = localStorage.getItem('tenant');
  const token = localStorage.getItem('token');

  useEffect(() => {
    axios.get(`http://${tenant}.localhost:8000/users/`, {
      headers: {
        Authorization: `Token ${token}`,
      },
    }).then(res => setUsers(res.data))
      .catch(err => console.error('Failed to fetch users:', err));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`http://${tenant}.localhost:8000/tasks/`, {
        title,
        description,
        status,
        assigned_to: assignedTo,
        due_date: dueDate || null,
      }, {
        headers: {
          Authorization: `Token ${token}`,
        },
      });
      setMessage(' Task created successfully');
      setTitle('');
      setDescription('');
      setStatus('todo');
      setAssignedTo('');
      setDueDate('');
      
      navigate('/tasks')

    } catch (err) {
      console.error(err);
      setMessage(' Failed to create task');
    }

    
  };

  return (
    <div className='create-task-container'>
      <h2>Create New Task</h2>
      <form onSubmit={handleSubmit}>
        <input 
          type="text"
          placeholder="Task Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />

        <input 
          type="text"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        />

        <select value={status} onChange={(e) => setStatus(e.target.value)} required>
          <option value="todo">To Do</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>

        <select value={createdBy} onChange={(e) => setCreatedBy(e.target.value)} required>
          <option value="">Created By</option>
          {users.map(user => (
            <option key={user.id} value={user.id}>{user.username}</option>
          ))}
        </select>

        <select value={assignedTo} onChange={(e) => setAssignedTo(e.target.value)} required>
          <option value="">Assign to</option>
          {users.map(user => (
            <option key={user.id} value={user.id}>{user.username}</option>
          ))}
        </select>

        <input 
          type="date"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
        />

        <button type="submit">Create Task</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default CreateTask;
