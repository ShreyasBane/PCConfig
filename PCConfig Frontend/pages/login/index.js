import React, { useState } from "react";
import { Form, Container, Row, Col, Button, Card } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import axios from "axios";
import Cookies from "js-cookie";
import Link from "next/link";
import { useRouter } from "next/router";
import Navbar from "../../components/Navbar";

export default function Login() {
  const router = useRouter();
  const [formState, setformState] = useState({
    username: "",
    password: ""
  });

  const [responseState, setresponseState] = useState({
    status: "idle",
    message: null
  });
  function handleSubmit() {
    axios
      .post("https://PCConfig.shreyasbane.repl.co/login", formState)
      .then((res) => {
        setresponseState(res);
        if (res.data.status === true) {
          Cookies.set("pcconfig.userID", res.data.userID);
          Cookies.set("pcconfig.username", res.data.username);
          router.push("/");
        } else alert(res.data.message);
      })
      .catch((err) => {
        setresponseState({ status: "error" });
      });
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
            <Card.Body>
              <Card.Title
                style={{ color: "#ffffff" }}
                className="text-center"
                as="h1"
              >
                Login
              </Card.Title>
              <Form style={{ color: "#ffffff" }} className="">
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
                  <Link href="/signup">No Account?</Link>
                </div>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}
