import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Tasks from './pages/Tasks';
import CreateTask from './pages/CreateTask';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path='/create-task' element={<CreateTask />} />
      </Routes>
    </Router>
  );
}

export default App;



