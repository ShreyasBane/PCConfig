import { Container, Row, Col } from "react-bootstrap";
import MyNavbar from "../components/Navbar/index.js";
import "bootstrap/dist/css/bootstrap.css";
import NavCard from "../components/NavCard";
import Footer from "../components/Footer";

export default function Home() {
  const createinfo = {
    title: "Create Config",
    description: "Try to manually create a config",
    page: "/builds"
  };
  const generateinfo = {
    title: "Generate Config",
    description:
      "Have a config generated automatcally for you based on set parameters",
    page: "/generate"
  };
  return (
    <Container
      style={{
        height: "100vh",
        position: "relative",
        backgroundColor: "#343a40"
      }}
      fluid
    >
      <MyNavbar />
      <Row style={{ backgroundColor: "#000000" }}>
        <Col sm={6} className="mt-3">
          <NavCard
            title={createinfo.title}
            description={createinfo.description}
            page={createinfo.page}
          />
        </Col>
        <Col sm={6} className="mt-3">
          <NavCard
            title={generateinfo.title}
            description={generateinfo.description}
            page={generateinfo.page}
          />
        </Col>
      </Row>
      <Row>
        <Col sm={12}>
          <Footer />
        </Col>
      </Row>
    </Container>
  );
}
