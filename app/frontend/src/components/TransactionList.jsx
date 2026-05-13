import { useState } from 'react'
import { Table, Form, Badge } from 'react-bootstrap'

const TransactionList = ({ transactions }) => {
  const [tickerFilter, setTickerFilter] = useState('')

  const filteredTransactions = transactions.filter(t =>
    t.ticker.toLowerCase().includes(tickerFilter.toLowerCase())
  )

  if (transactions.length === 0) {
    return <p>No transactions yet.</p>
  }

  return (
    <div>
      <h5>Transaction History</h5>

      <div style={{ display: 'flex', gap: '10px', marginBottom: '12px' }}>
        <Form.Select style={{ maxWidth: '300px' }}>
          <option>All Portfolios</option>
        </Form.Select>

        <Form.Control
          style={{ maxWidth: '300px' }}
          placeholder="Filter by ticker"
          value={tickerFilter}
          onChange={e => setTickerFilter(e.target.value)}
        />
      </div>

      <Table striped bordered hover responsive>
        <thead className="table-dark">
          <tr>
            <th>Date</th>
            <th>Portfolio</th>
            <th>Ticker</th>
            <th>Type</th>
            <th>Quantity</th>
            <th>Amount</th>
          </tr>
        </thead>

        <tbody>
          {filteredTransactions.map((t, index) => (
            <tr key={index}>
              <td>{t.date_time}</td>
              <td>{t.portfolio_name || 'Selected Portfolio'}</td>
              <td className="fw-bold">{t.ticker}</td>
              <td>
                <Badge bg={t.transaction_type === 'BUY' ? 'success' : 'danger'}>
                  {t.transaction_type}
                </Badge>
              </td>
              <td>{t.quantity}</td>
              <td>${Number(t.price).toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  )
}

export default TransactionList