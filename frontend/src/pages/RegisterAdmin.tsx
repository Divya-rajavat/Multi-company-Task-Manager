import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../Style/Signup.css'

const RegisterAdmin = () => {
    const [schemaName, setSchemaName] = useState('');
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isSubdomain, setIsSubdomain] = useState(false);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const hostname = window.location.hostname;
        const parts = hostname.split('.');

        if (parts.length > 2 || (parts.length === 2 && parts[0] !== 'localhost')) {
            setIsSubdomain(true);
        }
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setMessage('');

        const data: Record<string, string> = {
            username,
            email,
            password
        };

        if (!isSubdomain) {
            if (!schemaName) {
                setMessage('Company name is required.');
                return;
            }
            data.schema_name = schemaName.toLowerCase();
        }

        try {
            const backendBaseUrl = window.location.hostname === 'localhost'
                ? 'http://localhost:8000'
                : `http://${window.location.hostname}:8000`;

            const response = await axios.post(`${backendBaseUrl}/register-admin/`, data, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            setMessage(response.data.detail);

            alert("Tenant Super User created successfully!");
            setUsername('');
            setEmail('');
            setPassword('');
            setSchemaName('');
            setIsSubdomain(false);


        } catch (err: any) {
            setMessage(err.response?.data?.detail || 'Something went wrong.');
        }
    };

    return (
        <div className='signup-container'>
            <h2>Register Tenant Admin</h2>
            <form onSubmit={handleSubmit}>
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
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Register Admin</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default RegisterAdmin;
