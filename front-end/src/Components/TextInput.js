import React, { useContext } from "react";
import { AppContext } from './AppContext';
import { TextField } from '@mui/material';
import Box from '@mui/material/Box';
import FileUpload from './FileUpload';
import LoadDemoPatient from './LoadDemoPatient';


const TextInput = () => {
  const { inputText, setInputText, resetState } = useContext(AppContext);

  const handleReset = () => {
    resetState();
  }


  return (
    <>

      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          width: '100%',
          alignItems: 'center',
          gap: 2,
          padding: 2,
        }}
      >
        <LoadDemoPatient />
        <FileUpload />
      </Box>
      <TextField
        fullWidth
        label="Provide your free text, upload a file or load a demo patient"
        value={inputText}
        multiline
        rows={12}
        onChange={(e) => { setInputText(e.target.value) }}
      />


    </>

  );
}

export default TextInput;