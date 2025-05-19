import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../Style/Login.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [schemaName, setSchemaName] = useState('');
  const [isSubdomain, setIsSubdomain] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();


  useEffect(() => {
    const hostname = window.location.hostname;
    setIsSubdomain(!(hostname === 'localhost' || hostname.split('.').length === 1));
  }, []);


  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    const hostname = window.location.hostname;

    const data: Record<string, string> = {
      username,
      password,
    };

    if (!isSubdomain) {
      if (!schemaName.trim()) {
        setError('Please enter a company name.');
        return;
      }
      data.schema_name = schemaName.trim().toLowerCase();
    }

    try {
      const response = await axios.post(`http://${hostname}:8000/login/`, data);
      localStorage.setItem('token', response.data.token);
      if (response.data.tenant) {
        localStorage.setItem('tenant', response.data.tenant);
      }
      navigate('/tasks/');

      alert("Login successfully!");

    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed.');
    }
  };

  return (
    <div className="login-container">
      <h1>Login</h1>
      <form onSubmit={handleLogin}>
        {!isSubdomain && (
          <input
            type="text"
            placeholder="Company Name"
            value={schemaName}
            onChange={(e) => setSchemaName(e.target.value)}
            required
          />
        )}

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">Signup</button>

        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
}

export default Login;
