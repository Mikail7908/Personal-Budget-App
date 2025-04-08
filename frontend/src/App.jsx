import './App.css'

function App() {
  return (
    <div className="app">
      <header>
        <h1>💰 My Budget Tracker</h1>
        <p>Manage your money wisely. Track your income, expenses, and stay on top of your finances.</p>
      </header>

      <main>
        <section className="intro-card">
          <h2>Welcome!</h2>
          <p>This is your personal space to take control of your budget.</p>
          <p>Start by adding your income and expenses to see your current balance.</p>
        </section>

        <section className="cta">
          <button>Add New Expense</button>
          <button>Add Income</button>
        </section>
      </main>

    </div>
  )
}

export default App
