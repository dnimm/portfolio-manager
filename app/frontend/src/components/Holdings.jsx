import { Table } from 'react-bootstrap'

const Holdings = ({ portfolio, holdings }) => {
  if (!portfolio) return <p>Select a portfolio</p>

  return (
    <div>
      <h3>{portfolio.name}</h3>

      {portfolio.description && (
        <p>{portfolio.description}</p>
      )}

      {holdings.length === 0 ? (
        <p>No holdings yet. Use the Trade tab to buy securities.</p>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Ticker</th>
              <th>Quantity</th>
            </tr>
          </thead>

          <tbody>
            {holdings.map((h, index) => (
              <tr key={index}>
                <td>{h.ticker}</td>
                <td>{h.quantity}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </div>
  )
}

export default Holdings