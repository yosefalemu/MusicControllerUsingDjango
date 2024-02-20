import { createSlice } from "@reduxjs/toolkit";

const user = createSlice({
  name: "user",
  initialState: {
    currentUser: {},
    newUser: {},
  },
  reducers: {
    loginUserSuccess: (state, action) => {
      state.currentUser = action.payload;
      return state;
    },
    removeCurrentUser: (state) => {
      state.currentUser = {};
      return state;
    },
  },
});
export const { loginUserSuccess, removeCurrentUser } = user.actions;
export default user.reducer;
