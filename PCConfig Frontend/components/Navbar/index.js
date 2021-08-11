import { Navbar, Nav, Form, FormControl, Button } from "react-bootstrap";
import Cookies from "js-cookie";
import { useRouter } from "next/router";

function NavBar() {
  const router = useRouter();
  var username = Cookies.get("pcconfig.username");
  function UserLoginSignupDisplay(username) {
    if (!username) {
      return (
        <>
          <Nav.Link href="/login">Login</Nav.Link>
          <Nav.Link href="/signup">Signup</Nav.Link>
        </>
      );
    }
  }

  function UserDisplay(username) {
    if (username) {
      return (
        <Form inline>
          <Form.Label
            style={{
              color: "white",
              fontWeight: "bold"
            }}
          >
            Welcome {username}
          </Form.Label>
          <Button
            variant="outline-light"
            onClick={() => {
              Cookies.set("pcconfig.userID", "");
              Cookies.set("pcconfig.username", "");
              router.push("/");
            }}
          >
            Logout
          </Button>
        </Form>
      );
    }
  }

  return (
    <Navbar bg="dark" variant="dark">
      <Navbar.Brand href="/">PCConfig</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto font-weight-bold text-white">
          <Nav.Link href="/">Home</Nav.Link>
          <Nav.Link href="/builds">Create</Nav.Link>
          <Nav.Link href="/generate">Generate</Nav.Link>
          {UserLoginSignupDisplay(username)}
        </Nav>
        {UserDisplay(username)}
      </Navbar.Collapse>
    </Navbar>
  );
}

export default NavBar;
