import React, { useContext } from "react";
import { AppContext } from './AppContext';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { styled } from '@mui/material/styles';
import Chip from '@mui/material/Chip';



const FileUpload = () => {
    const { setInputText, setError } = useContext(AppContext);

    const VisuallyHiddenInput = styled('input')({
        clip: 'rect(0 0 0 0)',
        clipPath: 'inset(50%)',
        height: 1,
        overflow: 'hidden',
        position: 'absolute',
        bottom: 0,
        left: 0,
        whiteSpace: 'nowrap',
        width: 1,
    });


    const handleFileUpload = (event) => {
        try {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = (e) => setInputText(e.target.result);
            reader.readAsText(file);
            console.log(file);
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
            <Chip label="Upload a" icon={<CloudUploadIcon />} variant="outlined" onClick={() => { document.getElementById('fileInput').click() }} />
            <VisuallyHiddenInput
                id="fileInput"
                type="file"
                onChange={(e) => handleFileUpload(e)}
                multiple
            />
        </>

    );
}

export default FileUpload;