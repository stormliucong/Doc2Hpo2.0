import React, {useContext} from "react";
import { AppContext } from './AppContext';
import { Button } from '@mui/material';


const LoadDemoPatient = () => {
    const { setFileText, setError } = useContext(AppContext);
   
    const loadPatientTxt = async (file) => {
        // Load the patient text from the public folder using require
        try {
    
          const response = await fetch(file);
          if (!response.ok) throw new Error("Failed to fetch file");
          const text = await response.text();
          setFileText(text);
        } catch (error) {
          console.error(error);
          setError(error)
          setFileText("");
        }
      }
    
    return (
        <>
        <Button variant="outlined" component="label" onClick={() => loadPatientTxt('./demo_patient_1.txt')}>
            Load Demo Patient 1
        </Button>
        </>
    );
}

export default LoadDemoPatient;