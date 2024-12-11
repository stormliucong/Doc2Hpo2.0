import React, {useContext} from "react";
import { AppContext } from './AppContext';
import { Button } from '@mui/material';


const FileUpload = () => {
    const { setFileText } = useContext(AppContext);

    const handleFileUpload = (event) => {
        
        const file = event.target.files[0];
        const reader = new FileReader();
        reader.onload = (e) => setFileText(e.target.result);
        reader.readAsText(file);
      };
    
    return (
        <>
        <Button variant="outlined" component="label">
            Upload File
            <input type="file" hidden onChange={handleFileUpload} />
          </Button>
        </>
    );
}

export default FileUpload;