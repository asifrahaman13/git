import { createSlice } from "@reduxjs/toolkit";

export const repositorySlice = createSlice({
  name: "Repository",
  initialState: {
    xmlData: [
      {
        group_id: "sdf",
        artifact_id: "sdaf",
        version: "",
      },
    ],
  },
  reducers: {
    setXmlDataFormat: (state, action) => {
      const {xmlData} = action.payload;
      console.log(xmlData)
      state.xmlData = xmlData;
      console.log("The required json", JSON.parse(JSON.stringify(state.xmlData)));
    },
  },
});

export const { setXmlDataFormat } = repositorySlice.actions;

export default repositorySlice.reducer;
