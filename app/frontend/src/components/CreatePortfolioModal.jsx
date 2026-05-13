import { useState } from 'react'
import { Modal, Form, Button, Alert } from 'react-bootstrap'

const CreatePortfolioModal = ({ showModal, onModalClose, onCreate }) => {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState('')

  const handleCreate = () => {
    if (name.trim() === '') {
      setError('Portfolio name is required')
      return
    }

    onCreate(name, description)
    setName('')
    setDescription('')
    setError('')
    onModalClose()
  }

  return (
    <Modal show={showModal} onHide={onModalClose}>
      <Modal.Header closeButton>
        <Modal.Title>New Portfolio</Modal.Title>
      </Modal.Header>

      <Modal.Body>
        {error && <Alert variant="danger">{error}</Alert>}

        <Form>
          <Form.Group className="mb-3">
            <Form.Label>Name</Form.Label>
            <Form.Control
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="Growth Fund"
            />
          </Form.Group>

          <Form.Group>
            <Form.Label>Description</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              value={description}
              onChange={e => setDescription(e.target.value)}
              placeholder="Portfolio description"
            />
          </Form.Group>
        </Form>
      </Modal.Body>

      <Modal.Footer>
        <Button variant="secondary" onClick={onModalClose}>
          Cancel
        </Button>

        <Button variant="success" onClick={handleCreate}>
          Create
        </Button>
      </Modal.Footer>
    </Modal>
  )
}

export default CreatePortfolioModal