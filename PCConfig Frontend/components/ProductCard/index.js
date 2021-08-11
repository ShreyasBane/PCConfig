import { Card, Button, Image, Table } from "react-bootstrap";

function ProductCard({ data }) {
	const { id, image, productName, details } = data;
	return (
		<Card className="text-center">
			<Card.Header>{productName}</Card.Header>
			<Card.Body>
				<Image src={image} />
				<Table>
					<tbody>
						{details &&
							Object.entries(details).map((detail) => (
								<tr>
									<td>{detail[0]}</td>
									<td>{detail[1]}</td>
								</tr>
							))}
					</tbody>
				</Table>
			</Card.Body>
		</Card>
	);
}

export default ProductCard;
