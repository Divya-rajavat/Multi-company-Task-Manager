import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../Style/Signup.css';

type Plan = {
  id: number;
  name: string;
  price: string;
  duration_days: number;
  trial_days: number;
};

const Signup = () => {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [selectedPlan, setSelectedPlan] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [adminUsername, setAdminUsername] = useState('');
  const [adminEmail, setAdminEmail] = useState('');
  const [adminPassword, setAdminPassword] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPlans = async () => {
      try {
        const response = await axios.get('http://localhost:8000/plans/');
        setPlans(response.data);
        if (response.data.length > 0) {
          setSelectedPlan(response.data[0].name); 
        }
      } catch (err) {
        console.error('Failed to load plans:', err);
        setError('Could not load subscription plans.');
      }
    };

    fetchPlans();
  }, []);

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const response = await axios.post('http://localhost:8000/signup/', {
        company_name: companyName,
        tenant_admin_username: adminUsername,
        tenant_admin_email: adminEmail,
        tenant_admin_password: adminPassword,
        plan: selectedPlan
      });

      alert('Tenant and Admin created successfully!');
      console.log(response.data);

      setCompanyName('');
      setAdminUsername('');
      setAdminEmail('');
      setAdminPassword('');
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || 'Something went wrong.');
    }
  };

  return (
    <div className="signup-container">
      <form onSubmit={handleSignup}>
        <h2>Create New Company</h2>

        <input
          type="text"
          placeholder="Company Name"
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
          required
        />

        <select className='plan-menu'
          value={selectedPlan}
          onChange={(e) => setSelectedPlan(e.target.value)}
          required
        >
          {plans.map((plan) => (
            <option key={plan.id} value={plan.name}>
              {plan.name.charAt(0).toUpperCase() + plan.name.slice(1)} - ${plan.price}
            </option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Admin Username"
          value={adminUsername}
          onChange={(e) => setAdminUsername(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Admin Email"
          value={adminEmail}
          onChange={(e) => setAdminEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Admin Password"
          value={adminPassword}
          onChange={(e) => setAdminPassword(e.target.value)}
          required
        />

        <button type="submit">Create Tenant and Admin</button>
        {error && <p>{error}</p>}
      </form>
    </div>
  );
};

export default Signup;
