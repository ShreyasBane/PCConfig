import React, { useState } from "react";
import { Form, Container, Row, Col, Button, Card } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import axios from "axios";
import Link from "next/link";
import { useRouter } from "next/router";
import Navbar from "../../components/Navbar";

export default function Signup() {
  const router = useRouter();
  const [formState, setformState] = useState({
    username: "",
    email: "",
    password: "",
    confirmpass: ""
  });

  const [responseState, setresponseState] = useState({
    status: "idle",
    message: null
  });

  function handleSubmit() {
    if (formState.password === formState.confirmpass) {
      axios
        .post("https://PCConfig.shreyasbane.repl.co/signup", formState)
        .then((res) => {
          setresponseState(res);
          if (res.data.status === true) router.push("/login");
          else alert(res.data.message);
        })
        .catch((err) => {
          setresponseState({ status: err });
        });
    } else alert("Passwords do not match");
  }

  return (
    <Container
      style={{
        height: "100vh",
        position: "relative",
        backgroundColor: "#343a40"
      }}
      fluid
    >
      <Navbar />
      <Row style={{ backgroundColor: "#000000" }}>
        <Col style={{ height: "91vh" }} sm={12} lg={{ span: 4, offset: 4 }}>
          <Card style={{ backgroundColor: "#1F1F1F" }} className="w-100 mt-5">
            <Card.Body style={{ color: "#ffffff" }}>
              <Card.Title className="text-center" as="h1">
                SignUp
              </Card.Title>
              <Form>
                {/* <pre className="text-muted">
                  {JSON.stringify(formState, null, 4)}
                </pre>
                <pre className="text-muted">
                  {JSON.stringify(responseState, null, 4)}
                </pre> */}
                <Form.Group controlId="formBasicEmail">
                  <Form.Label>Username</Form.Label>
                  <Form.Control
                    type="email"
                    defaultValue={formState.username}
                    onChange={(e) => {
                      setformState({
                        ...formState,
                        username: e.target.value
                      });
                    }}
                    placeholder="Username"
                  />
                </Form.Group>
                <Form.Group controlId="formBasicEmail">
                  <Form.Label>Email address</Form.Label>
                  <Form.Control
                    type="email"
                    defaultValue={formState.email}
                    onChange={(e) => {
                      setformState({
                        ...formState,
                        email: e.target.value
                      });
                    }}
                    placeholder="Enter email"
                  />
                </Form.Group>
                <Form.Group controlId="formBasicPassword">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                    type="password"
                    defaultValue={formState.password}
                    onChange={(e) => {
                      setformState({
                        ...formState,
                        password: e.target.value
                      });
                    }}
                    placeholder="Password"
                  />
                </Form.Group>
                <Form.Group controlId="formBasicPassword">
                  <Form.Label>Confirm Password</Form.Label>
                  <Form.Control
                    type="password"
                    defaultValue={formState.confirmpass}
                    onChange={(e) => {
                      setformState({
                        ...formState,
                        confirmpass: e.target.value
                      });
                    }}
                    placeholder="Confirm Password"
                  />
                </Form.Group>
                <Button
                  block
                  variant="primary"
                  type="submit"
                  onClick={(e) => {
                    e.preventDefault();
                    handleSubmit();
                  }}
                >
                  Submit
                </Button>
                <div className="text-right">
                  <Link href="/login">Already Have an Account?</Link>
                </div>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}
