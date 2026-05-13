import { useEffect, useState } from 'react'
import { Container, Tabs, Tab, Alert } from 'react-bootstrap'
import PortfolioList from './PortfolioList'
import Holdings from './Holdings'
import TradePanel from './TradePanel'
import TransactionList from './TransactionList'
import CreatePortfolioModal from './CreatePortfolioModal'
import { apiRequest } from '../api'
import { getUsername } from '../auth'

const DashboardContainer = () => {
  const [portfolios, setPortfolios] = useState([])
  const [selectedPortfolio, setSelectedPortfolio] = useState(null)
  const [holdings, setHoldings] = useState([])
  const [transactions, setTransactions] = useState([])
  const [activeTab, setActiveTab] = useState('portfolios')
  const [showCreatePortfolioModal, setShowCreatePortfolioModal] = useState(false)
  const [error, setError] = useState('')

  const username = getUsername()

  useEffect(() => {
    loadPortfolios()
  }, [])

  const loadPortfolios = async () => {
    try {
      const data = await apiRequest(`/portfolios/user/${username}`)
      setPortfolios(data)
    } catch (err) {
      setError(err.message)
    }
  }

  const handleCreatePortfolio = async (name, description) => {
    try {
      await apiRequest('/portfolios/', 'POST', {
        username: username,
        name: name,
        description: description,
      })

      setShowCreatePortfolioModal(false)
      loadPortfolios()
    } catch (err) {
      setError(err.message)
    }
  }

  const handleSelectPortfolio = async (portfolioId) => {
    const found = portfolios.find(p => p.id === portfolioId)
    setSelectedPortfolio(found)
    setActiveTab('holdings')

    try {
      const holdingsData = await apiRequest(`/portfolios/${portfolioId}/holdings`)
      setHoldings(holdingsData)

      const transactionsData = await apiRequest(`/portfolios/${portfolioId}/transactions`)
      setTransactions(transactionsData)
    } catch (err) {
      setError(err.message)
    }
  }

  const handleDeletePortfolio = async (portfolioId) => {
    try {
      await apiRequest(`/portfolios/${portfolioId}`, 'DELETE')
      setPortfolios(portfolios.filter(p => p.id !== portfolioId))
      setSelectedPortfolio(null)
      setHoldings([])
      setTransactions([])
    } catch (err) {
      setError(err.message)
    }
  }

  const handleBuy = async (portfolioId, ticker, quantity) => {
    try {
      await apiRequest('/trades/buy', 'POST', {
        portfolio_id: portfolioId,
        ticker: ticker,
        quantity: Number(quantity),
      })

      await handleSelectPortfolio(portfolioId)
      setActiveTab('transactions')
    } catch (err) {
      setError(err.message)
    }
  }

  const handleSell = async (portfolioId, ticker, quantity) => {
    try {
      await apiRequest('/trades/sell', 'POST', {
        portfolio_id: portfolioId,
        ticker: ticker,
        quantity: Number(quantity),
      })

      await handleSelectPortfolio(portfolioId)
      setActiveTab('transactions')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <Container className="mt-4">
      {error && (
        <Alert variant="danger" dismissible onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      <Tabs activeKey={activeTab} onSelect={k => setActiveTab(k)} className="mb-3">
        <Tab eventKey="portfolios" title="Portfolios">
          <PortfolioList
            portfolios={portfolios}
            onCreatePortfolio={() => setShowCreatePortfolioModal(true)}
            onSelectPortfolio={handleSelectPortfolio}
            onDeletePortfolio={handleDeletePortfolio}
          />

          <CreatePortfolioModal
            showModal={showCreatePortfolioModal}
            onModalClose={() => setShowCreatePortfolioModal(false)}
            onCreate={handleCreatePortfolio}
          />
        </Tab>

        <Tab eventKey="holdings" title="Holdings">
          <Holdings portfolio={selectedPortfolio} holdings={holdings} />
        </Tab>

        <Tab eventKey="trade" title="Trade">
          <TradePanel
            portfolio={selectedPortfolio}
            holdings={holdings}
            onBuy={handleBuy}
            onSell={handleSell}
            error=""
            success=""
            setError={() => {}}
            setSuccess={() => {}}
          />
        </Tab>

        <Tab eventKey="transactions" title="Transactions">
          <TransactionList transactions={transactions} />
        </Tab>
      </Tabs>
    </Container>
  )
}

export default DashboardContainer