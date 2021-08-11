import React, { useEffect, useState } from "react";
import { Container, Row, Col, Button, ListGroup } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import Cookies from "js-cookie";
import axios from "axios";
import Link from "next/link";
import Navbar from "../../components/Navbar";

export default function Build() {
  const userID = Cookies.get("pcconfig.userID");
  const buildID = Cookies.get("pcconfig.buildID");

  const [data, setData] = useState({});
  const [status, setStatus] = useState({});
  const [name, setName] = useState({});
  let count = 0;

  useEffect(() => {
    axios(`https://PCConfig.shreyasbane.repl.co/user/build/${buildID}`)
      .then((res) => {
        setData(res.data.build);
        setStatus(res.data.status);
        // setName(res.data);
      })
      .catch((err) => alert(err.message));
  }, [buildID]);

  useEffect(() => {
    axios(`https://PCConfig.shreyasbane.repl.co/user/build/${buildID}/names`)
      .then((res) => {
        // alert(JSON.stringify(res.data));
        setName(res.data);
      })
      .catch((err) => alert(err.message));
  }, [data, buildID]);

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
        <Col style={{ height: "91vh" }} sm={12}>
          <div
            className="rounded p-3 mt-3"
            style={{ backgroundColor: "#1F1F1F" }}
          >
            <h1 className="text-white mt-3 mb-4">{data.name}</h1>
            <div className="bg-dark text-light">
              {/* <pre>{JSON.stringify(name, null, 4)}</pre>
              <pre>{JSON.stringify(data, null, 4)}</pre>
              <pre>{JSON.stringify(status, null, 4)}</pre> */}
            </div>
            <ListGroup>
              {Object.keys(data)
                ?.filter((x) => x !== "ID")
                .filter((x) => x !== "userID")
                .filter((x) => x !== "name")
                .map((key, index) => (
                  <ListGroup.Item style={{ backgroundColor: "#CFCFCF" }}>
                    <div key={index}>
                      <span className="text-uppercase">{key} : </span>
                      <Link href={`/searchpage/${key}s`}>
                        <Button>
                          {data[key] === "" ? "Add Component" : name[key]}
                        </Button>
                      </Link>
                    </div>
                  </ListGroup.Item>
                ))}
              <ListGroup.Item>
                Status : {status ? "Compatible" : "Not compatible"}
              </ListGroup.Item>
            </ListGroup>
          </div>
        </Col>
      </Row>
    </Container>
  );
}

//"ID": "B4",
//"userID": "U4",
//"cpu": "C13",
//"motherboard": "M1",
//"ram": "R57",
//"gpu": "G46",
//"storage": "S17",
//"psu": "P8"

// paste here
// create - https://PCConfig.shreyasbane.repl.co/user/{userID}/builds/new
// update - https://PCConfig.shreyasbane.repl.co/user/build/{builID}/modify/C1
// delete - https://PCConfig.shreyasbane.repl.co/user/build/{buildID}/delete
// get - https://PCConfig.shreyasbane.repl.co/user/build/${buildId}

//export async function getServerSideProps(ctx) {
//	if (!data)
//		return {
//			props: {
//				notFound: true
//			}
//		};
//	else
//		return {
//			props: {
//				data
//			}
//		};
//}
//
