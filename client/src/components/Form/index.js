import React from "react";
import { useForm } from "react-hook-form";
import axios from "axios";
import { ErrorMessage } from "@hookform/error-message";
import "./index.css";
function Form() {
	const {
		register,
		handleSubmit,
		formState: { errors },
	} = useForm();

	const formData = new FormData();

	const onSubmit = (data) => {
		if (data.files) {
			formData.append("files", data.files[0]);

			axios
				.post("http://localhost:5000/uploader", formData, {
					headers: {
						"Access-Control-Allow-Origin": "*",
						"content-type": "multipart/form-data",
					},
				})
				.then((res) => {
					const html_boxes = res.data.names.reduce(
						(html, name) =>
							html +
							`<img src="http://localhost:5000/displays/${name}">`,
						""
					);

					document.getElementById("result").innerHTML = html_boxes;
				})
				.catch((err) => {
					console.log(err);
				});
		}
		return 0;
	};

	return (
		<>
			<form onSubmit={handleSubmit(onSubmit)} className="form-group">
				<input
					type="file"
					className="form-control"
					{...register("files", { required: "This is required." })}
				/>
				<ErrorMessage
					errors={errors}
					name="files"
					className="alert alert-warning"
					as="div"
				/>
				<div className="button__configure">
					<button
						type="submit"
						className="btn btn-primary"
						onClick={onSubmit}
					>
						{" "}
						submit{" "}
					</button>
				</div>
			</form>
		</>
	);
}

export default Form;
