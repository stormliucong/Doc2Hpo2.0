import React, {useContext} from "react";
import { AppContext } from './AppContext';
import { TextField, Button, Typography } from '@mui/material';
import { useState } from 'react';



const TextInput = () => {
    const { setFileText } = useContext(AppContext);
    const [inputText, setInputText] = useState('');
    
    return (
        <>
        <Typography variant="h6" gutterBottom>
          Input Text
        </Typography>
        <TextField
          fullWidth
          label="Input Text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />

        <Button variant="contained" sx={{ mt: 1 }} onClick={() => {setFileText(inputText); setInputText('')} }>
          Submit
        </Button>
        </>
    );
}

export default TextInput;