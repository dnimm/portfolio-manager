import { Modal, Button } from 'react-bootstrap'

const DeletePortfolioModal = ({ showModal, onModalClose, onDelete }) => {
  return (
    <Modal show={showModal} onHide={onModalClose}>
      <Modal.Header closeButton>
        <Modal.Title>Are you sure?</Modal.Title>
      </Modal.Header>

      <Modal.Body>
        <p>This action is irreversible. Please make sure you want to proceed.</p>
      </Modal.Body>

      <Modal.Footer>
        <Button variant="danger" onClick={onDelete}>
          Yes
        </Button>

        <Button variant="secondary" onClick={onModalClose}>
          No
        </Button>
      </Modal.Footer>
    </Modal>
  )
}

export default DeletePortfolioModal