import { useEffect, useState } from "react";
import {
  BarChart3,
  CreditCard,
  LayoutDashboard,
  LogOut,
  Settings,
  Users,
  Wallet,
  ArrowDownRight,
  ArrowUpRight,
  PiggyBank,
  RefreshCw,
} from "lucide-react";
import "./App.css";

type CategorySpending = {
  category_id: number;
  category_name: string;
  amount: number;
  percentage: number;
};

type MonthlySummary = {
  month: string;
  total_income: number;
  total_expense: number;
  net_savings: number;
  savings_percentage: number;
  category_breakdown: CategorySpending[];
};

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [summary, setSummary] = useState<MonthlySummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const userId = 1;

  const fetchSummary = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        `${API_URL}/api/v1/analytics/monthly?user_id=${userId}&year=2026&month=9`,
      );

      if (!response.ok) {
        throw new Error("Failed to fetch dashboard data");
      }

      const data: MonthlySummary = await response.json();
      setSummary(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong while loading your finances.",
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  const formatCurrency = (amount: number) =>
    new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(amount);

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Wallet size={21} />
          </div>
          <span>FinTrack</span>
        </div>

        <nav className="navigation">
          <a className="nav-item active">
            <LayoutDashboard size={19} />
            Dashboard
          </a>

          <a className="nav-item">
            <CreditCard size={19} />
            Transactions
          </a>

          <a className="nav-item">
            <Wallet size={19} />
            Accounts
          </a>

          <a className="nav-item">
            <Users size={19} />
            Family
          </a>

          <a className="nav-item">
            <BarChart3 size={19} />
            Analytics
          </a>
        </nav>

        <div className="sidebar-bottom">
          <a className="nav-item">
            <Settings size={19} />
            Settings
          </a>

          <a className="nav-item">
            <LogOut size={19} />
            Sign out
          </a>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">PERSONAL FINANCE</p>
            <h1>Dashboard</h1>
          </div>

          <div className="profile">
            <div className="avatar">A</div>
            <div>
              <strong>Astha</strong>
              <span>Personal account</span>
            </div>
          </div>
        </header>

        <section className="welcome">
          <div>
            <h2>Good afternoon, Astha 👋</h2>
            <p>
              Here's how your finances are looking this month.
            </p>
          </div>

          <button className="refresh-button" onClick={fetchSummary}>
            <RefreshCw size={17} />
            Refresh
          </button>
        </section>

        {loading && (
          <div className="state-card">
            <div className="loader" />
            <p>Loading your financial overview...</p>
          </div>
        )}

        {error && (
          <div className="error-card">
            <strong>Unable to load dashboard</strong>
            <p>{error}</p>
            <button onClick={fetchSummary}>Try again</button>
          </div>
        )}

        {!loading && !error && summary && (
          <>
            <section className="stats-grid">
              <div className="stat-card">
                <div className="stat-header">
                  <span>Total income</span>
                  <div className="stat-icon income">
                    <ArrowUpRight size={18} />
                  </div>
                </div>

                <h3>{formatCurrency(summary.total_income)}</h3>
                <p className="positive">This month's income</p>
              </div>

              <div className="stat-card">
                <div className="stat-header">
                  <span>Total spending</span>
                  <div className="stat-icon expense">
                    <ArrowDownRight size={18} />
                  </div>
                </div>

                <h3>{formatCurrency(summary.total_expense)}</h3>
                <p>Across all categories</p>
              </div>

              <div className="stat-card">
                <div className="stat-header">
                  <span>Net savings</span>
                  <div className="stat-icon savings">
                    <PiggyBank size={18} />
                  </div>
                </div>

                <h3>{formatCurrency(summary.net_savings)}</h3>
                <p>{summary.savings_percentage.toFixed(1)}% savings rate</p>
              </div>
            </section>

            <section className="dashboard-grid">
              <div className="panel">
                <div className="panel-header">
                  <div>
                    <h2>Spending by category</h2>
                    <p>Where your money is going this month</p>
                  </div>
                </div>

                {summary.category_breakdown.length === 0 ? (
                  <div className="empty-state">
                    <Wallet size={32} />
                    <p>No expense data for this month yet.</p>
                  </div>
                ) : (
                  <div className="category-list">
                    {summary.category_breakdown.map((category) => (
                      <div className="category-row" key={category.category_id}>
                        <div className="category-info">
                          <div className="category-name">
                            <span className="category-dot" />
                            {category.category_name}
                          </div>

                          <strong>{formatCurrency(category.amount)}</strong>
                        </div>

                        <div className="progress-track">
                          <div
                            className="progress-bar"
                            style={{
                              width: `${Math.min(category.percentage, 100)}%`,
                            }}
                          />
                        </div>

                        <span className="percentage">
                          {category.percentage.toFixed(1)}%
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="panel">
                <div className="panel-header">
                  <div>
                    <h2>Monthly overview</h2>
                    <p>September 2026</p>
                  </div>
                </div>

                <div className="overview">
                  <div className="overview-item">
                    <span>Income</span>
                    <strong className="income-text">
                      {formatCurrency(summary.total_income)}
                    </strong>
                  </div>

                  <div className="overview-item">
                    <span>Expenses</span>
                    <strong className="expense-text">
                      {formatCurrency(summary.total_expense)}
                    </strong>
                  </div>

                  <div className="overview-divider" />

                  <div className="overview-item">
                    <span>Remaining</span>
                    <strong>
                      {formatCurrency(summary.net_savings)}
                    </strong>
                  </div>

                  <div className="savings-box">
                    <PiggyBank size={22} />
                    <div>
                      <strong>
                        {summary.savings_percentage.toFixed(1)}%
                      </strong>
                      <span>of your income is saved</span>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
