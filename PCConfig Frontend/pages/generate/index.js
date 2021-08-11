import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Container,
  Row,
  Col,
  Button,
  ListGroup,
  Form,
  Card
} from "react-bootstrap";
import Cookies from "js-cookie";
import axios from "axios";
import Navbar from "../../components/Navbar";
import "bootstrap/dist/css/bootstrap.css";
import Router from "next/router";

function Build({ data }) {
  const arrayed = Object.entries(data)
    .filter((x) => x[0] !== "ID")
    .filter((x) => x[0] !== "userID")
    .filter((x) => x[0] !== "name");
  return (
    <Card className="my-1">
      <Card.Body>
        <h2 className="text-center">{data.name}</h2>
        <ListGroup>
          {arrayed.map(([key, { name, ID }]) => (
            <ListGroup.Item>
              <div>
                <span className="text-uppercase">{key} :</span>
                <span> {name}</span>
              </div>
            </ListGroup.Item>
          ))}
        </ListGroup>
      </Card.Body>
    </Card>
  );
}

export default function Generate() {
  const [answers, setAnswers] = useState({});
  const [generated, setGenerated] = useState([]);

  function reset() {
    setGenerated([]);
  }

  // https://PCConfig.shreyasbane.repl.co/generate

  function getGenerated(payload) {
    axios
      .post("https://PCConfig.shreyasbane.repl.co/generate", payload)
      .then((res) => setGenerated(res.data))
      .catch((err) => alert(err.message));
  }

  function handleCheck(name, value) {
    setAnswers({ ...answers, [name]: value });
  }

  return (
    <Container
      style={{
        height: "100vh",
        position: "relative"
        // backgroundColor: "#343a40"
      }}
      fluid
    >
      <Navbar />
      <Button onClick={reset} className="my-1">
        Reset
      </Button>
      <Row>
        {generated.length === 0 ? (
          <Col sm={12} lg={{ span: 6, offset: 3 }}>
            <Form
              onSubmit={(e) => {
                e.preventDefault();
                getGenerated(answers);
              }}
            >
              <Form.Group controlId="formBasicRadio">
                <Form.Label>1. Will you do video editing?</Form.Label>
                <Form.Check
                  type="radio"
                  name="Question-1"
                  id="Question-1-1"
                  label="No"
                  value="ENTRY"
                  onChange={(e) => handleCheck(e.target.name, e.target.value)}
                />
                <Form.Check
                  type="radio"
                  name="Question-1"
                  id="Question-1-2"
                  label="Ocassionally"
                  value="MID"
                  onChange={(e) => handleCheck(e.target.name, e.target.value)}
                />
                <Form.Check
                  type="radio"
                  name="Question-1"
                  id="Question-1-3"
                  label="Frequently"
                  value="PRO"
                  onChange={(e) => handleCheck(e.target.name, e.target.value)}
                />
              </Form.Group>
              <Form.Group>
                <Form.Label>2. What kind of games will you play?</Form.Label>
                <Form.Check
                  type="radio"
                  name="Question-2"
                  id="Question-2-1"
                  label="No Games"
                  value="ENTRY"
                  onChange={(e) => handleCheck(e.target.name, e.target.value)}
                />
                <Form.Check
                  type="radio"
                  name="Question-2"
                  id="Question-2-2"
                  label="Lighter Games"
                  value="MID"
                  onChange={(e) => handleCheck(e.target.name, e.target.value)}
                />
                <Form.Check
                  type="radio"
                  name="Question-2"
                  id="Question-2-3"
                  label="Heavier Games"
                  value="PRO"
                  onChange={(e) => handleCheck(e.target.name, e.target.value)}
                />
              </Form.Group>
              <Form.Group>
                <Form.Label>3. Will you edit pictures on it?</Form.Label>
                <Form.Check
                  type="radio"
                  name="Question-3"
                  id="Question-3-1"
                  label="No"
                  value="ENTRY"
                  onChange={(e) => handleCheck(e.target.name, e.target.value)}
                />
                <Form.Check
                  type="radio"
                  name="Question-3"
                  id="Question-3-2"
                  label="Ocassionally"
                  value="MID"
                  onChange={(e) => handleCheck(e.target.name, e.target.value)}
                />
                <Form.Check
                  type="radio"
                  name="Question-3"
                  id="Question-3-3"
                  label="Frequently"
                  value="PRO"
                  onChange={(e) => handleCheck(e.target.name, e.target.value)}
                />
              </Form.Group>
              <Form.Group>
                <Form.Label>4. Will you use the pc for 3d modeling?</Form.Label>
                <Form.Check
                  type="radio"
                  name="Question-4"
                  id="Question-4-1"
                  label="No"
                  value="ENTRY"
                  onChange={(e) => handleCheck(e.target.name, e.target.value)}
                />
                <Form.Check
                  type="radio"
                  name="Question-4"
                  id="Question-4-2"
                  label="Ocassionally"
                  value="MID"
                  onChange={(e) => handleCheck(e.target.name, e.target.value)}
                />
                <Form.Check
                  type="radio"
                  name="Question-4"
                  id="Question-4-3"
                  label="Frequently"
                  value="PRO"
                  onChange={(e) => handleCheck(e.target.name, e.target.value)}
                />
              </Form.Group>
              <Button variant="primary" type="submit">
                Submit
              </Button>
            </Form>
          </Col>
        ) : (
          <Col sm={12} lg={{ span: 6, offset: 3 }}>
            {generated?.map((x) => (
              <Build data={x} />
            ))}
          </Col>
        )}
      </Row>
    </Container>
  );
}
