import React, { useState, useEffect } from "react";
import { Container, Row, Col, Card, Modal } from "react-bootstrap";
import Filter from "../../components/Filter";
import SearchCard from "../../components/SearchCard";
import ProductCard from "../../components/ProductCard";
import Navbar from "../../components/Navbar";
import Cookies from "js-cookie";
import axios from "axios";

//PCConfig.shreyasbane.repl.co/user/build/{buidId}/modify/{productId}

export default function SearchPage({ productType, products, filters }) {
  // STATES
  const [state, setState] = useState([]);
  const [record, setRecord] = useState({});
  const [rec, setRec] = useState([]);

  const [modal, setModal] = useState(false);
  const [product, setProduct] = useState({});

  const filterKeys = filters.map((x) => x.name);
  let count = 0;

  async function fetchDetails(pid) {
    const res = await fetch(
      `https://PCConfig.shreyasbane.repl.co/product/info/${pid}`
    );
    const data = await res.json();
    setProduct(data);
    setModal(true);
  }

  function handleClose() {
    setProduct(false);
  }

  useEffect(() => {
    let obj = {};
    const defaultRecord = filters.map((x) => x.name);
    defaultRecord.forEach((x) => (obj[x] = []));
    setRecord(obj);
  }, [count]);

  useEffect(() => {
    async function fetchData() {
      const res = await fetch(
        "https://PCConfig.shreyasbane.repl.co/product/" + productType + "/",
        {
          method: "POST",
          body: JSON.stringify(record)
        }
      );
      const resdata = await res.json();
      setState(resdata);
    }
    fetchData();
  }, [record]);

  useEffect(() => {
    const buildID = Cookies.get("pcconfig.buildID");
    //  recommendedUrl = PCConfig.shreyasbane.repl.co/recommend/buildID/productType
    async function fetchRec() {
      const res = await fetch(
        "https://PCConfig.shreyasbane.repl.co/recommend/" +
          buildID +
          "/" +
          productType
      );
      const resdata = await res.json();
      setRec(resdata);
      // alert(JSON.stringify(resdata));
    }
    fetchRec();
  }, [count]);

  function manage({ name, target, checked }) {
    // get that record
    let newrecord = record[name];
    const exists = newrecord.includes(target);
    if (checked && !exists) {
      // add to it
      newrecord = [...newrecord, target];
    } else if (exists) {
      // remove
      newrecord = newrecord.filter((x) => x !== target);
    }
    // set new record
    setRecord({
      ...record,
      [name]: newrecord
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
        {/* <Col sm={12}>
          <pre>{JSON.stringify(record, null, 4)}</pre>
        </Col> */}
        <Col
          className="rounded m-3 p-4"
          style={{ backgroundColor: "#1F1F1F" }}
          sm={2}
        >
          <Filter items={filters} onChange={(e) => manage(e)} />
        </Col>
        <Col
          className="rounded m-3"
          style={{ backgroundColor: "#1F1F1F" }}
          sm={9}
        >
          <Card className="mt-2" style={{ backgroundColor: "#17d1ce" }}>
            <Card.Title>Recommended</Card.Title>
            <Card.Body>
              {rec?.map((product, index) => (
                <SearchCard key={index} item={product} />
              ))}
            </Card.Body>
          </Card>
          {state?.map((product, index) => {
            return <SearchCard key={index} item={product} />;
          })}
        </Col>
      </Row>
    </Container>
  );
}

export async function getStaticPaths() {
  return {
    paths: [
      { params: { product: "gpus" } },
      { params: { product: "cpus" } },
      { params: { product: "motherboards" } },
      { params: { product: "rams" } },
      { params: { product: "psus" } },
      { params: { product: "storages" } }
    ],
    fallback: true
  };
}

export async function getStaticProps(ctx) {
  const productName = ctx.params.product;
  const productsUrl =
    "https://PCConfig.shreyasbane.repl.co/product/" + productName;
  const filtersUrl =
    "https://PCConfig.shreyasbane.repl.co/product/" + productName + "/filter";

  const req = {};

  const productsRes = await fetch(productsUrl, {
    method: "POST",
    body: JSON.stringify(req)
  });
  const productsData = await productsRes.json();

  const filtersRes = await fetch(filtersUrl);
  const filtersData = await filtersRes.json();
  return {
    props: {
      productType: productName,
      products: productsData,
      filters: filtersData
    }
  };
}
