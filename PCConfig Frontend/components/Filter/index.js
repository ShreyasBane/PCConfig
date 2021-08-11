import { Container, Row, Col, Form } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.css";

function Filter({ items, onChange }) {
  return (
    <Container className="text-white">
      <Row>
        <Col sm={12}>
          <Form>
            {items.map((item) => (
              <>
                <Form.Label>{item.name}</Form.Label>
                <Form.Group>
                  {item.options.map((choice) => (
                    <Form.Check
                      type="checkbox"
                      label={choice}
                      onChange={(e) =>
                        onChange({
                          name: item.name,
                          target: choice,
                          checked: e.target.checked
                        })
                      }
                    />
                  ))}
                </Form.Group>
              </>
            ))}
          </Form>
        </Col>
      </Row>
    </Container>
  );
}

export default Filter;
