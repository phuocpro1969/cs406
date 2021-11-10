import React from "react";
import "./index.css";
import { Markup } from "interweave";

export default function Item(props) {
	console.log(props);
	return (
		<>
			<div className="layout-item">
				{props.data.name ? (
					<img
						key={props.data.i}
						alt={props.data.name}
						src={`http://localhost:5000/displays/${props.data.name}`}
					/>
				) : (
					""
				)}
			</div>
			<div className="layout-item">
				<Markup content={props.data.text} />
			</div>
		</>
	);
}
