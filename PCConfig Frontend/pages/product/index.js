import { Container, Row, Col } from "react-bootstrap";
import { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.css";
import ProductCard from "../../components/ProductCard";
import axios from "axios";
import Cookies from "js-cookie";

export default function Product() {
	const pid = Cookies.get("pcconfig.productID");
	const [product, setProduct] = useState([]);
	let count = 0;
	useEffect(() => {
		axios
			.get(`https://PCConfig.shreyasbane.repl.co/product/info/${pid}`)
			.then((res) => {
				setProduct(res.data);
			})
			.catch((err) => {
				alert("Error : ", JSON.stringify(err));
			});
	}, [count]);

	return (
		<Container
			style={{
				height: "100vh",
				position: "relative"
			}}
			fluid>
			{/* <pre>{JSON.stringify(product, null, 4)}</pre> */}
			<Row>
				<Col sm={12}>{product && <ProductCard data={product} />}</Col>
			</Row>
		</Container>
	);
}
