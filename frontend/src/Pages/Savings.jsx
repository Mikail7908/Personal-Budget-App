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

  const fetchGoals = () => {
    fetch("http://127.0.0.1:5000/api/savings-goals")
      .then((res) => res.json())
      .then(setGoals)
      .catch((err) => console.error("Error fetching savings goals:", err));
  };

  useEffect(() => {
    fetchGoals();
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const url = editingId
      ? `http://127.0.0.1:5000/api/savings-goals/${editingId}`
      : "http://127.0.0.1:5000/api/savings-goals";

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
      fetchGoals();
    } catch (err) {
      console.error(err.message);
    }
  };

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

  const handleDelete = (id) => {
    fetch(`http://127.0.0.1:5000/api/savings-goals/${id}`, {
      method: "DELETE",
    })
      .then(fetchGoals)
      .catch((err) => console.error("Error deleting goal:", err));
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
        {goals.map((goal) => (
          <li key={goal.id}>
            <strong>{goal.description}</strong>
            <span>Target: £{goal.target_amount.toFixed(2)}</span>
            <span>Saved: £{goal.current_amount.toFixed(2)}</span>
            <span>Deadline: {goal.deadline}</span>
            <span>Frequency: {goal.saving_frequency}</span>
            <div>
              <span>Progress: {goal.progress.toFixed(1)}%</span>
              <div className="progress-bar">
                <div
                  className="progress-bar-fill"
                  style={{ width: `${Math.min(goal.progress, 100)}%` }}
                />
              </div>
            </div>
            <button onClick={() => handleEdit(goal)}>Edit</button>
            <button onClick={() => handleDelete(goal.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Savings;
