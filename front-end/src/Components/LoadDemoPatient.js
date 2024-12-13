import React, { useContext } from "react";
import { AppContext } from './AppContext';
import Chip from '@mui/material/Chip';


const LoadDemoPatient = () => {
  const { setInputText, setError } = useContext(AppContext);

  const loadPatientTxt = async (file) => {
    // Load the patient text from the public folder using require
    try {

      const response = await fetch(file);
      if (!response.ok) throw new Error("Failed to fetch file");
      const text = await response.text();
      setInputText(text);
    } catch (error) {
      console.error(error);
      setError(error)
      setInputText("");
    }
  }

  return (
    <>
      <Chip label="Demo 1" onClick={() => loadPatientTxt('./demo_patient_1.txt')} />
      <Chip label="Demo 2" disabled />
    </>
  );
}

export default LoadDemoPatient;