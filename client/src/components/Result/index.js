import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import Item from "./Item/index";

export default function Result() {
	const data = useSelector((state) => state.data);
	const [props, setProps] = useState([]);

	useEffect(() => {
		let arr = [];
		if (data.names && data.names.length > 0) {
			for (let i of data.names) {
				console.log(i);
				arr.append({
					i: i,
					name: data.names[i],
					text: data.texts[i],
				});
			}
		}

		console.log(arr);

		setProps(arr);
	}, [data]);

	console.log(props);

	return (
		<>
			<div>
				<h1> RESULT </h1>
				{props && props?.map((prop) => <Item props={prop} />)}
			</div>
		</>
	);
}
