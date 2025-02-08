import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
    const [transactions, setTransactions] = useState([]);

    useEffect(() => {
        const fetchTransactions = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await axios.get('http://127.0.0.1:5000/transactions/all', {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                setTransactions(response.data.transactions);
            } catch (err) {
                console.error('Error fetching transactions', err);
            }
        };
        fetchTransactions();
    }, []);

    return (
        <div>
            <h2>Dashboard</h2>
            <h3>Transactions</h3>
            <ul>
                {transactions.map((transaction) => (
                    <li key={transaction.id}>
                        {transaction.type} of {transaction.amount} in {transaction.category}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Dashboard;