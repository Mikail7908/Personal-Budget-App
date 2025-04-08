import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Transactions from './pages/Transactions'
import Income from './pages/Income'
import Expenses from './pages/Expenses'
import Budget from './pages/Budget'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <nav>
          <ul className="nav">
            <li><Link to="/">Home</Link></li>
            <li><Link to="/transactions">Transactions</Link></li>
            <li><Link to="/income">Income</Link></li>
            <li><Link to="/expenses">Expenses</Link></li>
            <li><Link to="/budget">Budget</Link></li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/transactions" element={<Transactions />} />
          <Route path="/income" element={<Income />} />
          <Route path="/expenses" element={<Expenses />} />
          <Route path="/budget" element={<Budget />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App;
