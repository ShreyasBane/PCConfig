import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Container, Row, Col, Button, ListGroup, Form } from "react-bootstrap";
import Cookies from "js-cookie";
import axios from "axios";
import Navbar from "../../components/Navbar";
import "bootstrap/dist/css/bootstrap.css";
import Router from "next/router";

export default function Builds() {
  const userID = Cookies.get("pcconfig.userID");
  const [name, setName] = useState("");
  const [builds, setBuilds] = useState([]);
  const [response, setResponse] = useState();
  let count = 0;
  useEffect(() => {
    axios
      .get(`https://PCConfig.shreyasbane.repl.co/user/${userID}/builds`)
      .then((res) => {
        const data = res.data;
        setBuilds(data);
      })
      .catch((err) => alert(err.message));
  }, [count]);

  console.log(userID);

  function handleNewBuild() {
    axios(
      `https://PCConfig.shreyasbane.repl.co/user/${userID}/builds/new/${name}`
    )
      .then((res) => {
        setResponse(res.data);
        Router.reload(window.location.pathname);
      })
      .catch((err) => alert(err.message));
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
        <Col style={{ height: "91vh" }}>
          <div
            className="rounded p-3 mt-3"
            style={{ backgroundColor: "#1F1F1F" }}
          >
            <div className="d-flex justify-content-between mt-3 mb-4">
              <h1 className="text-white">My Builds</h1>
              <Form>
                <Form.Group controlId="formBasicEmail">
                  <Form.Label>Build Name</Form.Label>
                  <Form.Control
                    className="mb-2"
                    type="text"
                    placeholder="Enter name"
                    defaultValue={name}
                    onChange={(e) => setName(e.target.value)}
                  />
                  <Button
                    block
                    variant="primary"
                    type="submit"
                    onClick={(e) => {
                      e.preventDefault();
                      handleNewBuild();
                    }}
                  >
                    New Build
                  </Button>
                </Form.Group>
              </Form>
            </div>
            <ListGroup>
              {builds.map((build, index) => (
                <ListGroup.Item style={{ backgroundColor: "#CFCFCF" }}>
                  <Link href="/builds/build" passHref>
                    <a
                      className="text-dark"
                      onClick={() => Cookies.set("pcconfig.buildID", build.ID)}
                    >
                      {build.name}
                    </a>
                  </Link>
                </ListGroup.Item>
              ))}
            </ListGroup>
          </div>
        </Col>
      </Row>
    </Container>
  );
}

//https://PCConfig.shreyasbane.repl.co/user/U3/builds
// [
//   {
//     "ID": "B3",
//     "userID": "U3",
//     "cpu": "C27",
//     "motherboard": "M1",
//     "ram": "R53",
//     "gpu": "G44",
//     "storage": "S14",
//     "psu": "P1"
//   }
// ]

// export async function getServerSideProps(ctx) {
// 	const userID = ctx.query.userID;
// 	const res = await fetch(
// 		`https://PCConfig.shreyasbane.repl.co/user/${userID}/builds`
// 	);
// 	const data = await res.json();
// 	return {
// 		props: {
// 			builds: data,
// 			userID
// 		}
// 	};
// }
//
