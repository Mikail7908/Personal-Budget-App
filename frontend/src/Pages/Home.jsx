import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function Home() {
  const [transactions, setTransactions] = useState([]);
  const [budgets, setBudgets] = useState([]);
  const [savingsGoals, setSavingsGoals] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/transactions")
      .then((res) => res.json())
      .then(setTransactions);

    fetch("http://127.0.0.1:5000/api/budgets")
      .then((res) => res.json())
      .then(setBudgets);

    fetch("http://127.0.0.1:5000/api/savings-goals")
      .then((res) => res.json())
      .then(setSavingsGoals);
  }, []);

  const totalIncome = transactions
    .filter((t) => t.type === "income")
    .reduce((sum, t) => sum + t.amount, 0);

  const totalExpense = transactions
    .filter((t) => t.type === "expense")
    .reduce((sum, t) => sum + t.amount, 0);

  const netBalance = totalIncome - totalExpense;

  const budgetChartData = budgets.map((b) => ({
    name: b.month,
    Allocated: b.amount,
    Spent: b.spent_amount,
  }));

  return (
    <div className="dashboard-container">
      <h2>Dashboard Overview</h2>
      <p className="dashboard-subtitle">Welcome to your personal budget app!</p>


      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="card income">
          <h3>Total Income</h3>
          <p>£{totalIncome.toFixed(2)}</p>
        </div>
        <div className="card expense">
          <h3>Total Expenses</h3>
          <p>£{totalExpense.toFixed(2)}</p>
        </div>
        <div className="card balance">
          <h3>Net Balance</h3>
          <p>£{netBalance.toFixed(2)}</p>
        </div>
      </div>

      {/* Two-column layout */}
      <div className="grid-layout">
        <div className="chart-section">
          <h3>Budget Overview</h3>
          {budgets.length ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={budgetChartData}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="Allocated" fill="#3b82f6" />
                <Bar dataKey="Spent" fill="#ef4444" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p>No budget data.</p>
          )}
        </div>

        <div className="savings-section">
          <h3>Savings Goals</h3>
          {savingsGoals.length ? (
            savingsGoals.map((goal) => {
              const progress =
                goal.target_amount > 0
                  ? (goal.current_amount / goal.target_amount) * 100
                  : 0;
              return (
                <div className="goal-card" key={goal.id}>
                  <div className="goal-header">
                    <span>{goal.description}</span>
                    <span>{progress.toFixed(1)}%</span>
                  </div>
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{ width: `${progress}%` }}
                    ></div>
                  </div>
                  <p className="goal-meta">
                    £{goal.current_amount.toFixed(2)} of £
                    {goal.target_amount.toFixed(2)} – Due:{" "}
                    {new Date(goal.deadline).toLocaleDateString()}
                  </p>
                </div>
              );
            })
          ) : (
            <p>No savings goals yet.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Home;
