import { useState, useEffect } from "react";

// Budget component to manage monthly budgets
function Budget() {
  const [budgets, setBudgets] = useState([]);
  const [categories, setCategories] = useState([]);
  const [form, setForm] = useState({
    category_id: "",
    amount: "",
    month: "",
  });
  const [categoryForm, setCategoryForm] = useState({
    name: "",
    type: "expense",
  });
  const [editingId, setEditingId] = useState(null);

  // Fetch API base URL from environment variables
  const API_BASE = import.meta.env.VITE_API_URL.replace(/\/$/, "");

  // Fetch budgets and categories from the API
  const fetchBudgets = () => {
    fetch(`${API_BASE}/api/budgets`)
      .then((res) => res.json())
      .then(setBudgets)
      .catch(console.error);
  };

  // Fetch categories from the API
  const fetchCategories = () => {
    fetch(`${API_BASE}/api/categories`)
      .then((res) => res.json())
      .then(setCategories)
      .catch(console.error);
  };

  useEffect(() => {
    fetchBudgets();
    fetchCategories();
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  // Handle form submission for budgets
  const handleSubmit = async (e) => {
    e.preventDefault();

    const method = editingId ? "PUT" : "POST";
    const url = editingId
      ? `${API_BASE}/api/budgets/${editingId}`
      : `${API_BASE}/api/budgets`;

    try {
      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      await res.json();
      setForm({ category_id: "", amount: "", month: "" });
      setEditingId(null);
      fetchBudgets();
    } catch (err) {
      console.error("Error submitting budget:", err.message);
    }
  };
  // Handle editing a budget
  const handleEdit = (budget) => {
    setForm({
      category_id: budget.category_id,
      amount: budget.amount,
      month: budget.month,
    });
    setEditingId(budget.id);
  };
  // Handle deleting a budget
  const handleDelete = (id) => {
    fetch(`${API_BASE}/api/budgets/${id}`, { method: "DELETE" })
      .then(fetchBudgets)
      .catch(console.error);
  };
  // Get category name by ID
  const getCategoryName = (id) => {
    const cat = categories.find((c) => c.id === id);
    return cat ? cat.name : `Category ${id}`;
  };
  // Handle form submission for categories
  const handleCategorySubmit = (e) => {
    e.preventDefault();
    fetch(`${API_BASE}/api/categories`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(categoryForm),
    })
      .then((res) => res.json())
      .then(() => {
        setCategoryForm({ name: "", type: "expense" });
        fetchCategories();
      })
      .catch(console.error);
  };

  return (
    <div className="page">
      <h2>Monthly Budget</h2>
      <p>
        Set and view your budget limits for different categories like food,
        rent, entertainment, etc.
      </p>

      {/* CATEGORY CREATION FORM */}
      <form onSubmit={handleCategorySubmit} className="budget-form">
        <input
          type="text"
          name="name"
          placeholder="New Category Name"
          value={categoryForm.name}
          onChange={(e) =>
            setCategoryForm({ ...categoryForm, name: e.target.value })
          }
          required
        />
        <select
          name="type"
          value={categoryForm.type}
          onChange={(e) =>
            setCategoryForm({ ...categoryForm, type: e.target.value })
          }
        >
          <option value="expense">Expense</option>
          <option value="income">Income</option>
        </select>
        <button type="submit">Add Category</button>
      </form>

      {/* BUDGET CREATION FORM */}
      <form onSubmit={handleSubmit} className="budget-form">
        <select
          name="category_id"
          value={form.category_id}
          onChange={handleChange}
          required
        >
          <option value="">Select Category</option>
          {categories.map((cat) => (
            <option key={cat.id} value={cat.id}>
              {cat.name} ({cat.type})
            </option>
          ))}
        </select>

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
          name="month"
          placeholder="e.g. April 2025"
          value={form.month}
          onChange={handleChange}
          required
        />
        <button type="submit">{editingId ? "Update" : "Add"} Budget</button>
      </form>

      {/* LIST OF BUDGETS */}
      <ul className="budget-list">
        {budgets.map((budget) => (
          <li key={budget.id}>
            <strong>Month:</strong> {budget.month}
            <strong>Category:</strong> {getCategoryName(budget.category_id)}
            <strong>Amount:</strong> £{budget.amount.toFixed(2)}
            <strong>Spent:</strong> £{budget.spent_amount.toFixed(2)}
            <strong>Remaining:</strong> £{budget.remaining.toFixed(2)}
            <div style={{ marginTop: "0.5rem" }}>
              <button onClick={() => handleEdit(budget)}>Edit</button>
              <button onClick={() => handleDelete(budget.id)}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Budget;
