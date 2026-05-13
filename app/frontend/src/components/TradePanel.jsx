import { useState } from 'react'
import { Alert, Card, Row, Col, Form, Button } from 'react-bootstrap'

const TradePanel = ({ portfolio, holdings, onBuy, onSell }) => {
  const [ticker, setTicker] = useState('')
  const [quantity, setQuantity] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  if (!portfolio) {
    return <p>Select a portfolio first</p>
  }

  const handleBuy = async () => {
    setError('')
    setMessage('')

    if (!ticker || !quantity) {
      setError('Please enter ticker and quantity.')
      return
    }

    await onBuy(portfolio.id, ticker, quantity)
    setMessage(`Bought ${quantity} share(s) of ${ticker.toUpperCase()}.`)
    setTicker('')
    setQuantity('')
  }

  const handleSell = async () => {
    setError('')
    setMessage('')

    if (!ticker || !quantity) {
      setError('Please enter ticker and quantity.')
      return
    }

    await onSell(portfolio.id, ticker, quantity)
    setMessage(`Sold ${quantity} share(s) of ${ticker.toUpperCase()}.`)
    setTicker('')
    setQuantity('')
  }

  return (
    <div>
      <h5>{portfolio.name}</h5>

      {message && (
        <Alert variant="success" dismissible onClose={() => setMessage('')}>
          {message}
        </Alert>
      )}

      {error && (
        <Alert variant="danger" dismissible onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      <Card style={{ maxWidth: '520px' }}>
        <Card.Body>
          <Form>
            <Row className="mb-3">
              <Col>
                <Form.Label>Ticker</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="e.g. AAPL"
                  value={ticker}
                  onChange={e => setTicker(e.target.value)}
                />
              </Col>

              <Col>
                <Form.Label>Quantity</Form.Label>
                <Form.Control
                  type="number"
                  placeholder="e.g. 10"
                  value={quantity}
                  onChange={e => setQuantity(e.target.value)}
                />
              </Col>
            </Row>

            <Button variant="success" onClick={handleBuy} style={{ marginRight: '8px' }}>
              Buy
            </Button>

            <Button variant="danger" onClick={handleSell}>
              Sell
            </Button>
          </Form>
        </Card.Body>
      </Card>

      <div style={{ marginTop: '20px' }}>
        <h6>Current Holdings</h6>

        {holdings.length === 0 ? (
          <p>No holdings yet.</p>
        ) : (
          holdings.map((h, index) => (
            <p key={index}>
              <strong>{h.ticker}</strong> {h.quantity} shares
            </p>
          ))
        )}
      </div>
    </div>
  )
}

export default TradePanel