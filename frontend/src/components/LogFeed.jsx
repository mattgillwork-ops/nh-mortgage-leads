import React, { useState, useEffect } from 'react';

const LogFeed = () => {
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        const eventSource = new EventSource('http://localhost:8000/stream');
        
        eventSource.onmessage = (event) => {
            const newLog = JSON.parse(event.data);
            setLogs((prevLogs) => [newLog, ...prevLogs].slice(0, 50));
        };

        eventSource.onerror = (err) => {
            console.error("EventSource failed:", err);
            eventSource.close();
        };

        return () => {
            eventSource.close();
        };
    }, []);

    return (
        <div className="LogFeed">
            <h2>Live Memory Logs</h2>
            <div className="LogList">
                {logs.map((log, index) => (
                    <div key={index} className="LogItem">
                        <span className="LogFilename">{log.filename}</span>
                        <pre className="LogContent">{log.content.substring(0, 300)}...</pre>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default LogFeed;
