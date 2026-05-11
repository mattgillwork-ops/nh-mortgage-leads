import React, { useState, useEffect } from 'react';

const AgentStatus = () => {
    const [status, setStatus] = useState(null);

    useEffect(() => {
        const fetchStatus = async () => {
            try {
                const response = await fetch('http://localhost:8000/health');
                const data = await response.json();
                setStatus(data);
            } catch (err) {
                console.error("Failed to fetch health status:", err);
            }
        };
        fetchStatus();
        const interval = setInterval(fetchStatus, 30000); // Check every 30s
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="AgentStatus">
            <h3>System Status</h3>
            {status ? (
                <div>
                    <p className="StatusOnline">● {status.status.toUpperCase()}</p>
                    <p>Agents Online: {status.agent_count}</p>
                    <p className="StatusSmall">Vault: {status.vault_path.split('\\').pop()}</p>
                </div>
            ) : (
                <p className="StatusOffline">○ OFFLINE</p>
            )}
        </div>
    );
};

export default AgentStatus;
