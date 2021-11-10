import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import Item from "./Item/index";
import "./index.css";

export default function Result() {
	const data = useSelector((state) => state.data);
	const [props, setProps] = useState([]);

	useEffect(() => {
		let arr = [];
		if (data && data.data.steps) {
			for (let i in data.data.steps) {
				arr.push({
					i: i,
					step: data.data.steps[i],
					name: data.data.names[i],
					text: data.data.texts[i],
				});
			}
		}

		setProps(arr);
	}, [data]);

	return (
		<>
			<div>
				<h1> RESULT </h1>
				{props &&
					props?.map((prop) => (
						<>
							<h1 className="step">{prop.step}</h1>
							<div className="layout">
								<Item data={prop} />
							</div>
						</>
					))}
			</div>
		</>
	);
}
