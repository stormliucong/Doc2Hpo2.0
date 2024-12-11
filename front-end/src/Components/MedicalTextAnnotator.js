import React from "react";
import { Box } from "@mui/system";
import AppProvider from "./AppContext";
import FileUpload from "./FileUpload";
import HighlightsBox from "./HighlightsBox";
import HighlightTable from "./HighlightTable";
import LoadDemoPatient from "./LoadDemoPatient";
import TextInput from "./TextInput";
import Warnings from "./Warnings";



const MedicalTextAnnotator = () => {
  return (
    <AppProvider>
      <Box p={2}>

        <Box mb={2}>
          <Warnings />
        </Box>

        <Box mb={2}>
          <TextInput />
        </Box>

        <Box mb={2}>
          <FileUpload />
          
        </Box>

        <Box mb={2}>
          <LoadDemoPatient />
        </Box>

        <Box mb={2}>
          <HighlightsBox />
        </Box>

        <Box mb={2}>
          <HighlightTable />
        </Box>
      </Box>
    </AppProvider>
  );
};

export default MedicalTextAnnotator;
