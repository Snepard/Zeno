import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode'; // need to install this!

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:4000/api';

const AuthContext = createContext({});

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Setup axios defaults
    const setupAxiosInterceptors = (token) => {
        if (token) {
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        } else {
            delete axios.defaults.headers.common['Authorization'];
        }
    };

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (token) {
            try {
                const decoded = jwtDecode(token);
                // Check if expired
                if (decoded.exp * 1000 < Date.now()) {
                    logout();
                } else {
                    setUser({ email: decoded.sub, name: decoded.name });
                    setupAxiosInterceptors(token);
                }
            } catch (err) {
                console.error("Invalid token", err);
                logout();
            }
        }
        setLoading(false);
    }, []);

    const login = async (email, password) => {
        const response = await axios.post(`${API_BASE}/auth/login`, { email, password });
        const { token, user: userData } = response.data;
        localStorage.setItem('access_token', token);
        setupAxiosInterceptors(token);
        setUser(userData);
        return userData;
    };

    const signup = async (name, email, password) => {
        const response = await axios.post(`${API_BASE}/auth/register`, { name, email, password });
        const { token, user: userData } = response.data;
        localStorage.setItem('access_token', token);
        setupAxiosInterceptors(token);
        setUser(userData);
        return userData;
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        setupAxiosInterceptors(null);
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, signup, logout }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};
