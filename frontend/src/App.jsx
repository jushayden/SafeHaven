import { Routes, Route, useLocation } from 'react-router-dom'
import Header from './components/Header'
import ErrorBoundary from './components/ErrorBoundary'
import Landing from './pages/Landing'
import Dashboard from './pages/Dashboard'
import DonationSuccess from './pages/DonationSuccess'

function App() {
  const location = useLocation()
  const showHeader = location.pathname !== '/'

  return (
    <div className="min-h-screen bg-bg-primary">
      {showHeader && <Header />}
      <ErrorBoundary>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/donation-success" element={<DonationSuccess />} />
        </Routes>
      </ErrorBoundary>
    </div>
  )
}

export default App
