import { Card, Button } from 'react-bootstrap'

function PortfolioList({ portfolios, onCreatePortfolio, onSelectPortfolio, onDeletePortfolio }) {
  return (
    <div>

      
      <Button
        variant="success"
        size="sm"
        style={{ marginBottom: '10px' }}
        onClick={onCreatePortfolio}
      >
        + New Portfolio
      </Button>

      
      {portfolios.length === 0 && (
        <p>No portfolios yet</p>
      )}

      {/* Portfolio cards */}
      {portfolios.map(p => (
        <Card key={p.id} style={{ marginBottom: '10px' }}>
          <Card.Body>
            <Card.Title>{p.name}</Card.Title>
            <Card.Text>{p.description}</Card.Text>

            
            <Button
              variant="outline-success"
              size="sm"
              onClick={() => onSelectPortfolio(p.id)}
              style={{ marginRight: '5px' }}
            >
              View
            </Button>

            
            <Button
  variant="danger"
  size="sm"
  onClick={() => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this portfolio?"
    )

    if (confirmDelete) {
      onDeletePortfolio(p.id)
    }
  }}
>
  Delete
</Button>

          </Card.Body>
        </Card>
      ))}
    </div>
  )
}

export default PortfolioList