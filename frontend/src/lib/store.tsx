import { configureStore } from "@reduxjs/toolkit";
import { combineReducers } from "@reduxjs/toolkit";
import repositorySlice from "./features/repository/repositorySlice";

export default configureStore({
  reducer: {
    repository: repositorySlice,
  },
});

const rootReducer = combineReducers({
  repository: repositorySlice,
});

export type RootState = ReturnType<typeof rootReducer>;
