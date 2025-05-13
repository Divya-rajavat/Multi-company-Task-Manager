import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../Style/Signup.css'

const Signup = () => {
  const [companyName, setCompanyName] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();

    const subdomain = companyName.toLowerCase().replace(/\s+/g, '');
    const tenantDomain = `${subdomain}.localhost`;
  
    try {
      const signupUrl = `http://${tenantDomain}:8000/signup/`;

      const response = await axios.post(signupUrl, {
        company_name: companyName,
        username,
        email,
        password,
      });

      console.log({ companyName, username, email, password });

      localStorage.setItem('auth_token', response.data.token);
      localStorage.setItem('tenant_domain', `${tenantDomain}`);

      navigate('/');
    } catch (err) {
      console.error(err);
      setError('Signup failed. Please try again.');
    }
  };

  return (
    <div className="signup-container">
      <h2>Signup</h2>
      <form onSubmit={handleSignup}>
        <div>
          <label>Company Name:</label>
          <input 
            type="text" 
            value={companyName} 
            onChange={(e) => setCompanyName(e.target.value)} 
            required
          />
        </div>
        <div>
          <label>Username:</label>
          <input 
            type="text" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            required
          />
        </div>
        <div>
          <label>Email:</label>
          <input 
            type="email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required
          />
        </div>
        <button type="submit">Signup</button>
      </form>
      {error && <div>{error}</div>}
      <p>Already have an account? <a href="/">Login</a></p>
    </div>
  );
};

export default Signup;
