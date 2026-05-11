import React from 'react';
import LogFeed from './components/LogFeed';
import AgentStatus from './components/AgentStatus';
import './App.css';

function App() {
  return (
    <div className="DashboardContainer">
      <aside className="Sidebar">
        <div className="Logo">ANTI-GRAVITY</div>
        <AgentStatus />
        <nav className="NavMenu">
          <button className="Active">Live Monitor</button>
          <button>Memory Graph</button>
          <button>Settings</button>
        </nav>
      </aside>
      <main className="MainContent">
        <header className="TopBar">
          <h1>Command Center</h1>
          <div className="UserBadge">Admin: mgill</div>
        </header>
        <div className="ContentArea">
          <LogFeed />
        </div>
      </main>
    </div>
  );
}

export default App;
