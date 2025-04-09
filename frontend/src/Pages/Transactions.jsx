import { useState, useEffect } from "react";

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [budgets, setBudgets] = useState([]);
  const [form, setForm] = useState({
    amount: "",
    description: "",
    date: "",
    type: "expense",
    budget_id: "",
  });
  const [editingId, setEditingId] = useState(null);

  // Fetch all transactions
  const fetchTransactions = () => {
    fetch("http://127.0.0.1:5000/api/transactions")
      .then((res) => res.json())
      .then((data) => {
        setTransactions(data);
        console.log("📦 Fetched transactions:", data);
      })
      .catch((err) =>
        console.error("Error fetching transactions:", err)
      );
  };

  const fetchBudgets = () => {
    fetch("http://127.0.0.1:5000/api/budget")
    .then((res) => res.json())
    .then ((data) => {
      setBudgets(data);
      console.log("Fetched budgets:", data);
    })
    .catch((err) =>
      console.error("Error fetching budgets:", err)
    );
  }

  useEffect(() => {
    fetchTransactions();
    fetchBudgets();
  }, []);

  // Handle input changes
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Submit (add or edit)
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("🚀 Submitting transaction:", form);

    const method = editingId ? "PUT" : "POST";
    const url = editingId
      ? `http://127.0.0.1:5000/api/transactions/${editingId}`
      : "http://127.0.0.1:5000/api/transactions";

    try {
      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Backend error: ${res.status} - ${errorText}`);
      }

      const result = await res.json();
      console.log("Backend response:", result);

      setForm({
        amount: "",
        description: "",
        date: "",
        type: "expense",
        budget_id: ""
      });
      setEditingId(null);
      fetchTransactions();
    } catch (err) {
      console.error("Error submitting transaction:", err.message);
      alert("Error: " + err.message);
    }
  };

  // Edit mode
  const handleEdit = (txn) => {
    setForm({
      amount: txn.amount,
      description: txn.description,
      date: txn.date,
      type: txn.type,
      budget_id: txn.budget_id || "",
    });
    setEditingId(txn.id); // assuming backend now returns 'id'
  };

  // Delete
  const handleDelete = (id) => {
    fetch(`http://127.0.0.1:5000/api/transactions/${id}`, {
      method: "DELETE",
    })
      .then(() => {
        console.log(`🗑️ Deleted transaction ${id}`);
        fetchTransactions();
      })
      .catch((err) =>
        console.error("Error deleting transaction:", err)
      );
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
        </select>
        <select name="budget_id" value={form.budget_id || ""} onChange={handleChange}>
          <option value="">No Budget</option>
          {budgets.map((budget) => (
            <option key={budget.id} value={budget.id}>
              {budget.category_id} - {budget.month}
            </option>
          ))}
        </select>
        <button type="submit">{editingId ? "Update" : "Add"} Transaction</button>
      </form>

      <ul className="transaction-list">
        {transactions.map((txn) => (
          <li key={txn.id} className="transaction-item">
            <span>${txn.amount.toFixed(2)}</span>
            <span>{txn.description}</span>
            <span>{txn.date}</span>
            <span>{txn.type}</span>
            <span>
              {txn.budget_id
                ? `Budget ID: ${txn.budget_id}`
                : "No Budget Assigned"}
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
