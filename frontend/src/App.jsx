import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './Pages/Home';
import Transactions from './Pages/Transactions';
import Budget from './Pages/Budget';
import Savings from './Pages/Savings';
import './App.css';

function App() {
  return (
    <Router>
      {/* FULL WIDTH NAVBAR OUTSIDE MAIN CONTAINER */}
      <nav className="nav">
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/transactions">Transactions</Link></li>
          <li><Link to="/budget">Budget</Link></li>
          <li><Link to="/savings">Savings</Link></li>
        </ul>
      </nav>

      {/* MAIN PAGE CONTAINER */}
      <div className="app">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/transactions" element={<Transactions />} />
          <Route path="/budget" element={<Budget />} />
          <Route path="/savings" element={<Savings />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
