import React, { useContext } from "react";
import { AppContext } from './AppContext';
import { TextField, Button, Typography } from '@mui/material';
import { useState } from 'react';
import Box from '@mui/material/Box';
import FileUpload from './FileUpload';
import LoadDemoPatient from './LoadDemoPatient';
import RestartAltIcon from '@mui/icons-material/RestartAlt';


const TextInput = () => {
  const { inputText, setInputText, resetState } = useContext(AppContext);

  const handleReset = () => {
    resetState();
  }


  return (
    <>
    
    <LoadDemoPatient />

      <TextField
        fullWidth
        label="Provide your free text, upload a file or load a demo patient"
        value={inputText}
        multiline
        rows={12}
        onChange={(e) => {setInputText(e.target.value)}}
      />
      <Box
      sx={{
        display: 'flex',
        justifyContent: 'right',
        width: '100%',
        alignItems: 'center',
        gap: 2,
        padding: 2,
      }}
    >
      {/* Left-aligned buttons */}
        <FileUpload />  

      {/* Right-aligned button */}
      <Button
            color="error"

            variant="contained"
            tabIndex={-1}
            startIcon={<RestartAltIcon />}
            onClick={() => handleReset()}
            >
            Reset
        </Button>

    </Box>
    </>

  );
}

export default TextInput;