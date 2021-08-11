import { IconContext } from "react-icons";
import { FaGithub, FaLinkedin, FaTwitter } from "react-icons/fa";
import { Container, Row, Col } from "react-bootstrap";

function Footer() {
  return (
    <Container
      style={{
        backgroundColor: "gray"
      }}
      fluid
    >
      <Row>
        <Col sm={8} className="">
          <h5>About</h5>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas
            mattis volutpat sollicitudin. Phasellus quam est, feugiat et
            malesuada ut, varius vel dui. Morbi at fermentum ante, eget
            tristique ex.
          </p>
        </Col>
        <Col>
          <h5>Made by</h5>
          <h4>Team Venture</h4>
        </Col>
        <Col>
          <h5>Contact Us</h5>
          <IconContext.Provider value={{ style: { fontSize: "30px" } }}>
            <div>
              <FaTwitter />
              <FaGithub />
              <FaLinkedin />
            </div>
          </IconContext.Provider>
        </Col>
      </Row>
    </Container>
  );
}

export default Footer;
