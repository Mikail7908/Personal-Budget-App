import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
  LabelList,
  XAxis,
  YAxis,
} from "recharts";
import { FaArrowUp, FaArrowDown } from "react-icons/fa";

function Home() {
  const [transactions, setTransactions] = useState([]);
  const [budgets, setBudgets] = useState([]);
  const [savingsGoals, setSavingsGoals] = useState([]);

  const API_BASE = import.meta.env.VITE_API_URL.replace(/\/$/, "");

  useEffect(() => {
    fetch(`${API_BASE}/api/transactions`)
      .then((res) => res.json())
      .then(setTransactions);

    fetch(`${API_BASE}/api/budgets`)
      .then((res) => res.json())
      .then(setBudgets);

    fetch(`${API_BASE}/api/savings-goals`)
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
    name: b.category_name,
    Allocated: b.amount,
    Spent: b.spent_amount,
  }));

  const spendingByCategoryData = budgets.map((budget) => ({
    category: budget.category_name,
    spent: budget.spent_amount,
  }));

  const savingsProgressData = savingsGoals.map((goal) => ({
    name: goal.description,
    value: goal.current_amount,
    target: goal.target_amount,
  }));

  const spendingColors = [
    "#3b82f6",
    "#f97316",
    "#10b981",
    "#8b5cf6",
    "#f43f5e",
    "#14b8a6",
    "#eab308",
  ];

  const pieData = [
    { name: "Income", value: totalIncome },
    { name: "Expenses", value: totalExpense },
  ];

  return (
    <div className="dashboard-container">
      <header className="header">
        <h1>Dashboard Overview</h1>
        <p className="dashboard-subtitle">Welcome to your personal budget app!</p>
      </header>

      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="card income">
          <h3>Total Income</h3>
          <div className="card-value">
            <FaArrowUp />
            <p>£{totalIncome.toFixed(2)}</p>
          </div>
        </div>
        <div className="card expense">
          <h3>Total Expenses</h3>
          <div className="card-value">
            <FaArrowDown />
            <p>£{totalExpense.toFixed(2)}</p>
          </div>
        </div>
        <div className="card balance">
          <h3>Net Balance</h3>
          <div className="card-value">
            <p>£{netBalance.toFixed(2)}</p>
          </div>
        </div>
      </div>

      <div className="grid-layout">
        {/* Spending by Category Bar Chart */}
        <div className="chart-section spending-by-category">
          <h3>Spending by Category</h3>
          {budgets.length ? (
            <ResponsiveContainer width="100%" height={350}>
              <BarChart
                data={spendingByCategoryData}
                margin={{ top: 10, right: 10, bottom: 30, left: 30 }}
              >
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="spent" animationDuration={1500}>
                  <LabelList dataKey="spent" position="top" fill="#fff" />
                  {spendingByCategoryData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={spendingColors[index % spendingColors.length]}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p>No budget data.</p>
          )}
        </div>

        {/* Savings Progress (Donut Chart) */}
        <div className="chart-section savings-progress">
          <h3>Savings Progress</h3>
          {savingsProgressData.length ? (
            savingsProgressData.map((goal) => {
              const progress = (goal.value / goal.target) * 100;
              return (
                <div key={goal.name} className="goal-card">
                  <h4>{goal.name}</h4>
                  <ResponsiveContainer width="100%" height={200}>
                    <PieChart>
                      <Pie
                        data={[
                          { name: "Progress", value: goal.value },
                          { name: "Remaining", value: goal.target - goal.value },
                        ]}
                        dataKey="value"
                        nameKey="name"
                        innerRadius={60}
                        outerRadius={80}
                        animationDuration={1500}
                      >
                        <Cell key="cell-1" fill="#34d399" />
                        <Cell key="cell-2" fill="#f97316" />
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                  <p>Progress: {progress.toFixed(1)}%</p>
                </div>
              );
            })
          ) : (
            <p>No savings data.</p>
          )}
        </div>
      </div>

      {/* Monthly Income vs Expenses Pie Chart */}
      <div className="chart-section monthly-income-expense">
        <h3>Income vs Expenses</h3>
        {pieData.length ? (
          <ResponsiveContainer width="100%" height={350}>
            <PieChart>
              <Pie
                data={pieData}
                dataKey="value"
                nameKey="name"
                outerRadius={120}
                fill="#8884d8"
                label
                animationDuration={1500}
              >
                <Cell fill="#34d399" />
                <Cell fill="#f97316" />
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        ) : (
          <p>No income/expense data available.</p>
        )}
      </div>
    </div>
  );
}

export default Home;
