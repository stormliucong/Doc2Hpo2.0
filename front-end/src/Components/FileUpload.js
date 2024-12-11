import React, {useContext} from "react";
import { AppContext } from './AppContext';
import { Button } from '@mui/material';


const FileUpload = () => {
    const { setFileText, setError } = useContext(AppContext);

    const handleFileUpload = (event) => {
        try {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = (e) => setFileText(e.target.result);
            reader.readAsText(file);
        }
        catch (error) {
            setError(error.message);
        }
        finally {
            event.target.value = null;
        }
    
    }
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