import './LoginPage.css'
import { Alert } from 'react-bootstrap'
import { startLogin } from '../auth'

const LoginPage = ({ authError }) => {
  return (
    <>
      <div className="lp-root">
        <div className="lp-hero">
          <div className="lp-hero-content">
            <div className="lp-logo">
              <span className="lp-logo-icon"></span>
              <span className="lp-logo-text">MoneyApp</span>
            </div>

            <h1 className="lp-headline">
              Smart portfolio<br /> management for <br /> modern investors.
            </h1>

            <p className="lp-subline">
              Track your holdings, execute trades, and review every transaction - all in one place.
            </p>

            <ul className="lp-features">
              <li><span className="lp-check">-</span>Create and manage multiple portfolios</li>
              <li><span className="lp-check">-</span>Buy and sell securities instantly</li>
              <li><span className="lp-check">-</span>Full transaction history with filters</li>
            </ul>
          </div>
        </div>

        <div className="lp-panel">
          <div className="lp-card">
            <div className="lp-card-logo">
              <span className="lp-logo-icon"></span>
            </div>

            <h2 className="lp-card-title">Welcome back</h2>
            <p className="lp-card-sub">Sign in to access your portfolio dashboard.</p>

            {authError && (
              <Alert variant="danger" className="lp-alert">
                {authError}
              </Alert>
            )}

            <button className="lp-signin-btn" onClick={ startLogin }>
              Sign in with Cognito
            </button>

            <p className="lp-footer-note">
              New here? You can create an account after clicking Sign in.
            </p>
          </div>
        </div>
      </div>
    </>
  )
}

export default LoginPage