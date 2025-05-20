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
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [paymentDone, setPaymentDone] = useState(false);

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

  const selectedPlanDetails = plans.find((p) => p.name === selectedPlan);

  const handleOpenModal = (e: React.FormEvent) => {
    e.preventDefault();
    setShowModal(true);
  };

  const handlePaymentAndSignup = async (status: 'success' | 'failed') => {
    if (!selectedPlanDetails) return;
  
    setError('');
    setLoading(true);
  
    try {
      const paymentResponse = await axios.post('http://localhost:8000/simulate-payment/', {
        company_name: companyName,
        plan: selectedPlan,
        payment_status: status,
      });
  
      const paymentStatus = paymentResponse.data.status;
  
      if (paymentStatus !== 'success') {
        setError(`Payment ${paymentStatus}. Tenant creation only allowed after successful payment.`);
        return; 
      }
  
      setPaymentDone(true);
      alert('Payment Successful!');
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || 'Payment failed.');
    } finally {
      setShowModal(false); 
      setLoading(false);
    }
  };
  

  const handleFinalSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!paymentDone) return;

    setLoading(true);
    setError('');

    try {
      const signupResponse = await axios.post('http://localhost:8000/signup/', {
        company_name: companyName,
        tenant_admin_username: adminUsername,
        tenant_admin_email: adminEmail,
        tenant_admin_password: adminPassword,
        plan: selectedPlan,
      });

      alert('Tenant and Admin created successfully!');
      console.log(signupResponse.data);

      setCompanyName('');
      setAdminUsername('');
      setAdminEmail('');
      setAdminPassword('');
      setError('');
      setPaymentDone(false);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-container">
      <form onSubmit={paymentDone ? handleFinalSignup : handleOpenModal}>
        <h2>Create New Company</h2>

        <input
          type="text"
          placeholder="Company Name"
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
          required
          disabled={loading}
        />

        <select
          className="plan-menu"
          value={selectedPlan}
          onChange={(e) => setSelectedPlan(e.target.value)}
          required
          disabled={loading}
        >
          {plans.map((plan) => (
            <option key={plan.id} value={plan.name}>
              {plan.name.charAt(0).toUpperCase() + plan.name.slice(1)} - ₹{plan.price}
            </option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Admin Username"
          value={adminUsername}
          onChange={(e) => setAdminUsername(e.target.value)}
          required
          disabled={loading}
        />
        <input
          type="email"
          placeholder="Admin Email"
          value={adminEmail}
          onChange={(e) => setAdminEmail(e.target.value)}
          required
          disabled={loading}
        />
        <input
          type="password"
          placeholder="Admin Password"
          value={adminPassword}
          onChange={(e) => setAdminPassword(e.target.value)}
          required
          disabled={loading}
        />

        <button type="submit" disabled={loading}>
          {loading
            ? 'Processing...'
            : paymentDone
            ? 'Create Tenant and Admin'
            : 'Continue to Payment'}
        </button>

        {error && <p style={{ color: 'red' }}>{error}</p>}
      </form>

      {showModal && selectedPlanDetails && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Confirm Your Plan</h3>
            <p><strong>Plan:</strong> {selectedPlanDetails.name}</p>
            <p><strong>Price:</strong> ₹{selectedPlanDetails.price}</p>
            <p><strong>Validity:</strong> {selectedPlanDetails.duration_days} days</p>
            <p><strong>Free Trial:</strong> {selectedPlanDetails.trial_days} days</p>

            <button onClick={() => handlePaymentAndSignup('success')} disabled={loading}>
              {loading ? 'Processing...' : 'Pay & Confirm'}
            </button>
            <button onClick={() => handlePaymentAndSignup('failed')} disabled={loading}>
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Signup;
