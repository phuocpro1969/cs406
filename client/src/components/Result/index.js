import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import Item from "./Item/index";

export default function Result() {
	const data = useSelector((state) => state.data);
	const [props, setProps] = useState([]);

	useEffect(() => {
		let arr = [];
		if (data && data.data.names) {
			for (let i in data.data.names) {
				arr.push({
					i: i,
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
				{props && props?.map((prop) => <Item data={prop} />)}
			</div>
		</>
	);
}
