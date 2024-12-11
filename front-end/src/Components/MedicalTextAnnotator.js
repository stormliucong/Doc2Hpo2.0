import React, { useEffect, useState } from "react";
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
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import PredictGene from "./PredictGeneButton";
import GeneTable from "./GeneTable";



const MedicalTextAnnotator = () => {
  const [step, setStep] = useState(1);
  const [nextStepText, setNextStepText] = useState("Annotate Text");
  
  useEffect(() => {
    if(step === 1) {
      setNextStepText("Annotate Text");
    } else if(step === 2) {
      setNextStepText("Review Annotations");
    } else if(step === 3) {
      setNextStepText("View Genes");
    } else {
      setNextStepText("Finish");
    }
  }, [step]);
  

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

      { step === 4 && <Grid2 container spacing={2}><GeneTable /></Grid2> }

      {/* Navigation Buttons */}
      <Grid2 container justifyContent="space-between" padding={2}>
        <Button
          variant="outlined"
          onClick={handleBack}
          disabled={step === 1}
          startIcon={<ArrowBackIcon />}
        >
          Go Back
        </Button>
        
        <Button
          variant="contained"
          onClick={handleNext}
          disabled={step === 4}
          endIcon={<ArrowForwardIcon />}
        >
          {nextStepText}
        </Button>
      </Grid2>  
    </AppProvider>
  );
};

export default MedicalTextAnnotator;
