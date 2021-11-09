import { combineReducers } from "redux";
import { resultReducer } from "./resultReducer";

const rootReducer = combineReducers({
	data: resultReducer,
});

export { rootReducer };
