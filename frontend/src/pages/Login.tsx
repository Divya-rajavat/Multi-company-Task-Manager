import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../Style/Login.css'

function Login() {
  const [companyName, setCompanyName] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    const subdomain = companyName.toLowerCase().replace(/\s+/g, '');
    const tenantDomain = `${subdomain}.localhost`;
  
    try {
      const loginUrl = `http://${tenantDomain}:8000/login/`;

      const response = await axios.post(loginUrl, {
        company_name: companyName,
        username,
        password,
      });

      const token = response.data.token;

      localStorage.setItem('token', token);
      localStorage.setItem('tenant_domain', `${tenantDomain}`);

      navigate('/tasks');
    } catch (err) {
      console.error(err);
      setError('Invalid credentials');
    }
  };

  return (
    <div className='login-container'>
      <h1>Login</h1>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Company Name"
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
          required
        />
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
        <button type="submit">Login</button>
      </form>
      {error && <div>{error}</div>}
    </div>
  );
}

export default Login;
