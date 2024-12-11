import React, { useContext } from "react";
import { AppContext } from './AppContext';
import { TextField, Button, Typography } from '@mui/material';
import { useState } from 'react';
import Box from '@mui/material/Box';
import FileUpload from './FileUpload';
import LoadDemoPatient from './LoadDemoPatient';
import RestartAltIcon from '@mui/icons-material/RestartAlt';


const TextInput = () => {
  const { inputText, setInputText, setFileText } = useContext(AppContext);


  return (
    <>
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'space-between',
        width: '100%',
        alignItems: 'center',
        padding: 2,
      }}
    >
      {/* Left-aligned buttons */}
      <Box sx={{ display: 'flex', gap: 1 }}>
        <FileUpload />  
        <LoadDemoPatient />
      </Box>

      {/* Right-aligned button */}
      <Button
            color="error"

            variant="contained"
            tabIndex={-1}
            startIcon={<RestartAltIcon />}
            onClick={() => setInputText("")}
            >
            Reset
        </Button>
    </Box>
    
      <TextField
        fullWidth
        label="Provide your free text, upload a file or load a demo patient"
        value={inputText}
        multiline
        rows={12}
        onChange={(e) => setInputText(e.target.value)}
      />
    </>

  );
}

export default TextInput;