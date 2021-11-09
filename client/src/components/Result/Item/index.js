import React from "react";

export default function Item(props) {
	console.log(props);
	console.log(`http://localhost:5000/uploads/${props.name}`);
	return (
		<>
			<div className="left">
				{
					<img
						key={props.i}
						alt={props.name}
						src={`http://localhost:5000/uploads/${props.name}`}
					/>
				}
			</div>
			<div className="right">{props.text}</div>
		</>
	);
}
