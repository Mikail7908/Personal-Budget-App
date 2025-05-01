import { useState, useEffect } from "react";

function Transactions({ onGoalChange }) {
  const [transactions, setTransactions] = useState([]);
  const [budgets, setBudgets] = useState([]);
  const [categories, setCategories] = useState([]);
  const [savingsGoals, setSavingsGoals] = useState([]);  
  const [form, setForm] = useState({
    amount: "",
    description: "",
    date: "",
    type: "expense",
    category_id: "",
    savings_id: "",
  });
  const [editingId, setEditingId] = useState(null);

  const API_BASE = import.meta.env.VITE_API_URL.replace(/\/$/, "");

  const fetchTransactions = () => {
    fetch(`${API_BASE}/api/transactions`)
      .then((res) => res.json())
      .then(setTransactions)
      .catch((err) => console.error("Error fetching transactions:", err));
  };

  const fetchBudgets = () => {
    fetch(`${API_BASE}/api/budgets`)
      .then((res) => res.json())
      .then(setBudgets)
      .catch((err) => console.error("Error fetching budgets:", err));
  };

  const fetchCategories = () => {
    fetch(`${API_BASE}/api/categories`)
      .then((res) => res.json())
      .then(setCategories)
      .catch((err) => console.error("Error fetching categories:", err));
  };

  const fetchSavingsGoals = () => {
    fetch(`${API_BASE}/api/savings-goals`) 
      .then((res) => res.json())
      .then(setSavingsGoals)
      .catch((err) => console.error("Error fetching savings goals:", err));
  };

  useEffect(() => {
    fetchTransactions();
    fetchBudgets();
    fetchCategories();
    fetchSavingsGoals();  
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const selectedCategoryId = parseInt(form.category_id);

    const matchingBudget = budgets.find(
      (b) => b.category_id === selectedCategoryId
    );

    const dataToSend = {
      amount: parseFloat(form.amount),
      description: form.description,
      date: form.date,
      type: form.type,
      budget_id: matchingBudget ? matchingBudget.id : null,
      savings_goal_id: form.savings_id || null,
    };

    console.log("Submitting transaction:", dataToSend);

    const method = editingId ? "PUT" : "POST";
    const url = editingId
      ? `${API_BASE}/api/transactions/${editingId}`
      : `${API_BASE}/api/transactions`;

    try {
      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dataToSend),
      });

      await res.json();

      if (form.type === "savings" && form.savings_id) {
        const updatedGoal = savingsGoals.find(
          (goal) => goal.id === form.savings_id
        );
        
        if (updatedGoal) {
          updatedGoal.current_amount += parseFloat(form.amount);  
          
          await fetch(`${API_BASE}/api/savings-goals/${updatedGoal.id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updatedGoal),
          });

          setSavingsGoals((prevGoals) =>
            prevGoals.map((goal) =>
              goal.id === updatedGoal.id ? updatedGoal : goal
            )
          );
        }
      }

      setForm({
        amount: "",
        description: "",
        date: "",
        type: "expense",
        category_id: "",
        savings_id: "",
      });
      setEditingId(null);
      fetchTransactions();
      fetchBudgets();
      fetchSavingsGoals();

      if (onGoalChange) {
        onGoalChange();
      }
    } catch (err) {
      console.error("Error submitting transaction:", err.message);
      alert("Error: " + err.message);
    }
  };

  const handleEdit = (txn) => {
    setForm({
      amount: txn.amount,
      description: txn.description,
      date: txn.date,
      type: txn.type,
      category_id: txn.category_id || "",
      savings_id: txn.savings_goal_id || "",
    });
    setEditingId(txn.id);
  };

  const handleDelete = (id) => {
    fetch(`${API_BASE}/api/transactions/${id}`, {
      method: "DELETE",
    })
      .then(fetchTransactions)
      .catch((err) => console.error("Error deleting transaction:", err));
  };

  const getBudgetName = (budgetId) => {
    const budget = budgets.find((b) => b.id === budgetId);
    if (!budget) return "Unknown Budget";

    const category = categories.find((c) => c.id === budget.category_id);
    const categoryName = category ? category.name : "Unknown Category";

    return `${categoryName} (${budget.month})`;
  };

  const getSavingsGoal = (savingsId) => {
    const goal = savingsGoals.find((g) => g.id === savingsId);
    return goal ? goal.description : "Unknown Savings Goal"; 
  };

  return (
    <div className="page">
      <h2>Transactions</h2>

      <form onSubmit={handleSubmit} className="transaction-form">
        <input
          type="number"
          name="amount"
          placeholder="Amount"
          value={form.amount}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="description"
          placeholder="Description"
          value={form.description}
          onChange={handleChange}
          required
        />
        <input
          type="date"
          name="date"
          value={form.date}
          onChange={handleChange}
          required
        />
        <select name="type" value={form.type} onChange={handleChange}>
          <option value="expense">Expense</option>
          <option value="income">Income</option>
          <option value="savings">Savings</option>
        </select>

        {form.type === "expense" && (
          <select
            name="category_id"
            value={form.category_id}
            onChange={handleChange}
            required
          >
            <option value="">Select Budget</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.name} ({cat.type})
              </option>
            ))}
          </select>
        )}

        {form.type === "savings" && (
          <select
            name="savings_id"
            value={form.savings_id}
            onChange={handleChange}
            required
          >
            <option value="">Select Savings Goal</option>
            {savingsGoals.map((goal) => (
              <option key={goal.id} value={goal.id}>
                {goal.description} 
              </option>
            ))}
          </select>
        )}

        <button type="submit">{editingId ? "Update" : "Add"} Transaction</button>
      </form>

      <ul className="transaction-list">
        {transactions.map((txn) => (
          <li key={txn.id} className="transaction-item">
            <span className="transaction-amount">£{txn.amount.toFixed(2)}</span>
            <span>{txn.description}</span>
            <span>{txn.date}</span>
            <span>{txn.type}</span>
            <span>
              {txn.budget_id
                ? `Budget: ${getBudgetName(txn.budget_id)}`
                : "No Budget Assigned"}
            </span>
            <span>
              {txn.savings_id
                ? `Savings Goal: ${getSavingsGoal(txn.savings_id)}`
                : ""}
            </span>
            <button onClick={() => handleEdit(txn)}>Edit</button>
            <button onClick={() => handleDelete(txn.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Transactions;
