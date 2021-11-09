import axios from "axios";

export const predict = (data) => (dispatch) => {
	const formData = new FormData();
	formData.append("files", data.files[0]);
	axios
		.post("http://localhost:5000/uploader", formData, {
			headers: {
				"Access-Control-Allow-Origin": "*",
				"content-type": "multipart/form-data",
			},
		})
		.then((res) => {
			dispatch({
				type: "FETCH_DATA",
				payload: res.data,
			});
		});
};
