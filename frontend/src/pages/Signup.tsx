import React, { useState } from 'react';
import axios from 'axios';
import '../Style/Signup.css'

const Signup = () => {
  const [companyName, setCompanyName] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSuperSignup = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        'http://localhost:8000/create-tenant/',
        { company_name: companyName,
          username,
          password, },
      );

      console.log(response.data);
      alert("Tenant created successfully!");
      setCompanyName('')
      setUsername('')
      setPassword('')

    } catch (err) {
      console.error(err);
      setError('Superuser signup failed.');
    }
  };

  if (window.location.hostname !== 'localhost') {
    alert('Tenant creation only allowed from public domain (localhost).');
    return;
  }
  

  return (
    <div className='signup-container'>
      <form onSubmit={handleSuperSignup}>
        <h2>Create New Company</h2>
        <input type="text" placeholder="Company Name" value={companyName} onChange={(e) => setCompanyName(e.target.value)} required />
        <input type="text" placeholder="Admin Username" value={username} onChange={(e) => setUsername(e.target.value)} required />
        <input type="password" placeholder="Admin Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit">Create Tenant</button>
        {error && <p>{error}</p>}
      </form>
    </div>
  );
};

export default Signup;
