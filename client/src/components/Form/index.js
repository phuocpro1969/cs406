import React from "react";
import { useForm } from "react-hook-form";
import { ErrorMessage } from "@hookform/error-message";
import { useDispatch } from "react-redux";
import "./index.css";
import { predict } from "../../redux/actions/resultAction";

function Form() {
	const dispatch = useDispatch();

	const {
		register,
		handleSubmit,
		formState: { errors },
	} = useForm();

	const onSubmit = (data) => {
		if (data.files) {
			dispatch(predict(data));
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
