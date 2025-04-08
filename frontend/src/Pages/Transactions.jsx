import { useState, useEffect } from "react";

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [form, setForm] = useState({
    amount: "",
    description: "",
    date: "",
    type: "expense",
  });
  const [editingId, setEditingId] = useState(null);

  // Fetch transactions from backend
  useEffect(() => {
    fetch("/api/transactions")
      .then((res) => res.json())
      .then((data) => setTransactions(data))
      .catch((err) => console.error("Error fetching:", err));
  }, []);

  // Handle form input changes
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Add or update transaction
  const handleSubmit = (e) => {
    e.preventDefault();

    const method = editingId ? "PUT" : "POST";
    const url = editingId ? `/api/transactions/${editingId}` : "/api/transactions";

    fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    })
      .then((res) => res.json())
      .then(() => {
        setForm({ amount: "", description: "", date: "", type: "expense" });
        setEditingId(null);
        return fetch("/api/transactions").then((res) => res.json());
      })
      .then((data) => setTransactions(data));
  };

  // Populate form for editing
  const handleEdit = (transaction) => {
    setForm(transaction);
    setEditingId(transaction.id);
  };

  // Delete transaction
  const handleDelete = (id) => {
    fetch(`/api/transactions/${id}`, { method: "DELETE" })
      .then(() => fetch("/api/transactions"))
      .then((res) => res.json())
      .then((data) => setTransactions(data));
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
        <button type="submit">{editingId ? "Update" : "Add"} Transaction</button>
      </form>

      <ul className="transaction-list">
        {transactions.map((txn) => (
          <li key={txn.id} className="transaction-item">
            <span>${txn.amount.toFixed(2)}</span>
            <span>{txn.description}</span>
            <span>{txn.date}</span>
            <span>{txn.type}</span>
            <button onClick={() => handleEdit(txn)}>Edit</button>
            <button onClick={() => handleDelete(txn.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Transactions;
