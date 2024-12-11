import React, { useState } from "react";
import { Box, Grid, Paper, Typography } from "@mui/material";
import AppProvider from "./AppContext";
import FileUpload from "./FileUpload";
import HighlightsBox from "./HighlightsBox";
import HighlightTable from "./HighlightTable";
import LoadDemoPatient from "./LoadDemoPatient";
import TextInput from "./TextInput";
import Warnings from "./Warnings";
import { Grid2 } from '@mui/material';
import Button from '@mui/material/Button';



const MedicalTextAnnotator = () => {
  const [step, setStep] = useState(1);

  // Navigate between steps
  const handleNext = () => setStep((prev) => prev + 1);
  const handleBack = () => setStep((prev) => prev - 1);

  return (
    <AppProvider>
      {/* Warning Banner */}
      <Grid2 container spacing={2}>
        <Grid2 size={12}>
        <Warnings />
        </Grid2>
      </Grid2>

      {/* Main Components */}
      <Grid2 container spacing={20} padding={5} justifyContent="center">
        {/* Step Header */}
      <Typography variant="h5" gutterBottom>
        {`Step ${step}: ${
          step === 1
            ? 'Input Text'
            : step === 2
            ? 'Annotate Text'
            : step === 3
            ? 'Review Annotations'
            : 'Gene Prediction'
        }`}
      </Typography>
      </Grid2>

      {/* Step Content */}
      
      { step === 1 && <Grid2 container spacing={2}><TextInput /></Grid2> }
      
      
      { step === 2 && <Grid2 container spacing={2}><HighlightsBox /></Grid2> }

      { step === 3 && <Grid2 container spacing={2}><HighlightTable /></Grid2> }

      {/* { step === 4 && <PredictGene /> } */}

      {/* Navigation Buttons */}
      <Grid2 container justifyContent="space-between" padding={2}>
        <Button
          variant="outlined"
          onClick={handleBack}
          disabled={step === 1}
        >
          Go Back
        </Button>
        <Button
          variant="contained"
          onClick={handleNext}
          disabled={step === 4}
        >
          Continue
        </Button>
      </Grid2>  
    </AppProvider>
  );
};

export default MedicalTextAnnotator;
