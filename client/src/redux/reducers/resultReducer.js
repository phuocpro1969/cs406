const initialState = {
	data: {},
};
const resultReducer = (state = initialState, action) => {
	switch (action.type) {
		case "FETCH_DATA": {
			const data = { ...action.payload };
			return { ...state, data: data };
		}
		default:
			return { ...state };
	}
};
export { resultReducer };
