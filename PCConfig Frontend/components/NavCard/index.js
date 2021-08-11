import { Jumbotron, Button, Image } from "react-bootstrap";
import { useRouter } from "next/router";

function NavBar({ title, description, page }) {
  const router = useRouter();
  return (
    <Jumbotron style={{ backgroundColor: "#1F1F1F" }} className="text-center">
      <Image src="https://picsum.photos/200" fluid className="mb-1" />
      <h1 style={{ color: "#ffffff" }}>{title}</h1>
      <p style={{ color: "#ffffff" }}>{description}</p>
      <Button
        variant="primary"
        block
        style={{ fontSize: "1.3rem" }}
        onClick={() => {
          router.push(page);
        }}
      >
        Try Out
      </Button>
    </Jumbotron>
  );
}

export default NavBar;
