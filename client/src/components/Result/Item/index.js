import React from "react";

export default function Item(props) {
	return (
		<>
			<div className="left">
				{
					<img
						key={props.data.i}
						alt={props.data.name}
						src={`http://localhost:5000/displays/${props.data.name}`}
					/>
				}
			</div>
			<div className="right">{props.data.text}</div>
		</>
	);
}
