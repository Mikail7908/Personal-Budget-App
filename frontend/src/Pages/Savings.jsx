import { useState, useEffect } from "react";

function Savings() {
  const [goals, setGoals] = useState([]);
  const [form, setForm] = useState({
    target_amount: "",
    current_amount: "",
    deadline: "",
    description: "",
    saving_frequency: "",
  });
  const [editingId, setEditingId] = useState(null);
  
  // Fetch API base URL from environment variables
  const API_BASE = import.meta.env.VITE_API_URL.replace(/\/$/, "");

  // Fetch savings goals from the API
  const fetchGoals = () => {
    fetch(`${API_BASE}/api/savings-goals`)
      .then((res) => res.json())
      .then(setGoals)
      .catch((err) => console.error("Error fetching savings goals:", err));
  };

  const updateGoals = () => {
    fetchGoals();
  };

  useEffect(() => {
    fetchGoals();
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Handle form submission for adding or updating a savings goal
  const handleSubmit = async (e) => {
    e.preventDefault();

    const url = editingId
      ? `${API_BASE}/api/savings-goals/${editingId}`
      : `${API_BASE}/api/savings-goals`;

    const method = editingId ? "PUT" : "POST";

    try {
      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      if (!res.ok) throw new Error("Failed to submit");

      await res.json();
      setForm({
        target_amount: "",
        current_amount: "",
        deadline: "",
        description: "",
        saving_frequency: "",
      });
      setEditingId(null);

      updateGoals();
    } catch (err) {
      console.error(err.message);
    }
  };

  // Handle editing a savings goal
  const handleEdit = (goal) => {
    setForm({
      target_amount: goal.target_amount,
      current_amount: goal.current_amount,
      deadline: goal.deadline,
      description: goal.description,
      saving_frequency: goal.saving_frequency,
    });
    setEditingId(goal.id);
  };

  // Handle deleting a savings goal
  const handleDelete = (id) => {
    fetch(`${API_BASE}/api/savings-goals/${id}`, {
      method: "DELETE",
    })
      .then(fetchGoals)
      .catch((err) => console.error("Error deleting goal:", err));
  };

  // Calculate progress
  const calculateProgress = (current_amount, target_amount) => {
    if (!target_amount) return 0; // Avoid divide by zero
    return (current_amount / target_amount) * 100;
  };

  return (
    <div className="page">
      <h2>Savings Goals</h2>
      <p>Track and manage your savings goals here.</p>

      <form onSubmit={handleSubmit} className="budget-form">
        <input
          type="number"
          name="target_amount"
          placeholder="Target Amount (£)"
          value={form.target_amount}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="current_amount"
          placeholder="Current Amount (£)"
          value={form.current_amount}
          onChange={handleChange}
          required
        />
        <input
          type="date"
          name="deadline"
          value={form.deadline}
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
          type="text"
          name="saving_frequency"
          placeholder="Saving Frequency (e.g. Weekly)"
          value={form.saving_frequency}
          onChange={handleChange}
          required
        />
        <button type="submit">{editingId ? "Update" : "Add"} Goal</button>
      </form>

      <ul className="budget-list">
        {goals.map((goal) => {
          const progress = calculateProgress(goal.current_amount, goal.target_amount);

          return (
            // Display each savings goal
            <li key={goal.id}>
              <strong>{goal.description}</strong>
              <span>Target: £{goal.target_amount.toFixed(2)}</span>
              <span>Saved: £{goal.current_amount.toFixed(2)}</span>
              <span>Deadline: {goal.deadline}</span>
              <span>Frequency: {goal.saving_frequency}</span>
              <div>
                <span>Progress: {progress.toFixed(1)}%</span>
                <div className="progress-bar">
                  <div
                    className="progress-bar-fill"
                    style={{ width: `${Math.min(progress, 100)}%` }}
                  />
                </div>
              </div>
              <button onClick={() => handleEdit(goal)}>Edit</button>
              <button onClick={() => handleDelete(goal.id)}>Delete</button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default Savings;
