import {
	Image,
	Container,
	Row,
	Col,
	Button,
	Table
} from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import Cookies from "js-cookie";
import axios from "axios";
import Link from "next/link";

function SearchCard({ item, info }) {
	function handler(productID) {
		const userID = Cookies.get("pcconfig.userID");
		const buildID = Cookies.get("pcconfig.buildID");
		const url = `https://PCConfig.shreyasbane.repl.co/user/build/${buildID}/modify/${productID}`;
		axios.get(url);
	}
	return (
		<Container
			className="rounded mt-3"
			style={{ backgroundColor: "#144144" }}>
			<Row>
				<Col
					sm={3}
					className="d-flex justify-content-start align-items-center">
					<Image src={item.imageUrl} />
				</Col>
				<Col sm={5}>
					<h2 style={{ color: "#FFFFFF" }}>{item.name}</h2>
					<Table borderless>
						<tbody className="d-flex flex-row">
							<div style={{ color: "#FFFFFF" }}>
								{Object.entries(item.details)
									.slice(0, 2)
									.map((detail) => (
										<tr>
											<td>
												<b>{detail[0] + ":"}</b>
											</td>
											<td>{detail[1]}</td>
										</tr>
									))}
							</div>
							<div style={{ color: "#FFFFFF" }}>
								{Object.entries(item.details)
									.slice(2)
									.map((detail) => (
										<tr>
											<td>
												<b>{detail[0]}</b>
											</td>
											<td>{detail[1]}</td>
										</tr>
									))}
							</div>
						</tbody>
					</Table>
				</Col>
				<Col
					sm={3}
					className="d-flex align-items-center justify-content-center">
					<a href="/product" target="_blank">
						<Button
							onClick={() =>
								Cookies.set("pcconfig.productID", item.ID)
							}>
							Info
						</Button>
					</a>
					<Link href="/builds/build" passHref>
						<Button
							style={{ backgroundColor: "#1DB954", color: "ffffff" }}
							variant="success"
							onClick={() => handler(item.ID)}
							size="lg">
							Add Component
						</Button>
					</Link>
				</Col>
			</Row>
		</Container>
	);
}

export default SearchCard;
