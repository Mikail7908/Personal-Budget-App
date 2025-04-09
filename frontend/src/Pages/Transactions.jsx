import { useState, useEffect } from "react";

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [budgets, setBudgets] = useState([]);
  const [categories, setCategories] = useState([]);
  const [form, setForm] = useState({
    amount: "",
    description: "",
    date: "",
    type: "expense",
    category_id: "",
    savings_id: "",
  });
  const [editingId, setEditingId] = useState(null);

  const fetchTransactions = () => {
    fetch("http://127.0.0.1:5000/api/transactions")
      .then((res) => res.json())
      .then(setTransactions)
      .catch((err) => console.error("Error fetching transactions:", err));
  };

  const fetchBudgets = () => {
    fetch("http://127.0.0.1:5000/api/budgets")
      .then((res) => res.json())
      .then(setBudgets)
      .catch((err) => console.error("Error fetching budgets:", err));
  };

  const fetchCategories = () => {
    fetch("http://127.0.0.1:5000/api/categories")
      .then((res) => res.json())
      .then(setCategories)
      .catch((err) => console.error("Error fetching categories:", err));
  };

  useEffect(() => {
    fetchTransactions();
    fetchBudgets();
    fetchCategories();
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
      savings_id: form.savings_id || null,
    };

    console.log("Submitting transaction:", dataToSend);

    const method = editingId ? "PUT" : "POST";
    const url = editingId
      ? `http://127.0.0.1:5000/api/transactions/${editingId}`
      : "http://127.0.0.1:5000/api/transactions";

    try {
      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dataToSend),
      });

      await res.json();
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
      savings_id: txn.savings_id || "",
    });
    setEditingId(txn.id);
  };

  const handleDelete = (id) => {
    fetch(`http://127.0.0.1:5000/api/transactions/${id}`, {
      method: "DELETE",
    })
      .then(fetchTransactions)
      .catch((err) => console.error("Error deleting transaction:", err));
  };

  const getCategoryName = (id) => {
    const cat = categories.find((c) => c.id === id);
    return cat ? cat.name : "Unknown Category";
  };

  const getBudgetName = (budgetId) => {
    const budget = budgets.find((b) => b.id === budgetId);
    if (!budget) return "Unknown Budget";

    const category = categories.find((c) => c.id === budget.category_id);
    const categoryName = category ? category.name : "Unknown Category";

    return `${categoryName} (${budget.month})`;
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

        {form.type !== "savings" && (
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
      <option value="">Select Savings</option>
      {categories
        .filter((cat) => cat.type === "savings")
        .map((cat) => (
          <option key={cat.id} value={cat.id}>
            {cat.name}
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
              {txn.category_id
                ? `Category: ${getCategoryName(txn.category_id)}`
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
