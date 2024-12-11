import React, { useEffect, useState, useContext } from 'react';
import { v4 as uuidv4 } from 'uuid';
import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    FormControlLabel,
    Switch,
    TextField,
    Slider,
    Backdrop,
    CircularProgress,
    Snackbar,
    Alert
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { AppContext } from './AppContext';
import TelegramIcon from '@mui/icons-material/Telegram';
import SettingsIcon from '@mui/icons-material/Settings';
import { ButtonGroup } from '@mui/material';

const PredictGeneButton = () => {
    const [dialogOpen, setDialogOpen] = useState(false);
    const [includeLowPriority, setIncludeLowPriority] = useState(false);
    const [includePredictedGene, setIncludePredictedGene] = useState(false);
    const [rank, setRank] = useState(5);
    const [sliderValue, setSliderValue] = useState(0.5);
    const [input, setInput] = useState('');
    const [data, setData] = useState([]);
    const {highlights, genePredictionResults, setGenePredictionResults, loading, setLoading, error, setError} = useContext(AppContext);


    useEffect(() => {
        setInput(highlights);
    }, [highlights]);

    useEffect(() => {
        setGenePredictionResults(data);
    }, [data]);


    const handlePhen2GeneCall = async () => {
        setLoading(true);
        setError(null);
        let isRequestActive = true;

        // Set a timeout to automatically cancel the request
        const timeoutId = setTimeout(() => {
            isRequestActive = false;
            setLoading(false);
            setError("Request timed out after 5 seconds.");
            console.log("Request timed out.");
        }, 50000);

        try {
            const response = await fetch('http://localhost:5000/api/predictgene', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    highlights,
                    includeLowPriority,
                    includePredictedGene,
                    rank,
                    threshold: sliderValue,
                }),
            }
            );
            // If the request is inactive (timed out), stop processing
            if (!isRequestActive) return;

            clearTimeout(timeoutId); // Clear timeout if the request completes on time
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            const res = await response.json();
            // push res into data
            setData(res);
        }
        catch (error) {
            if (isRequestActive) {
                setError(error.message);
                console.error("Error fetching data:", error.message);
            }
        }
        finally {
            if (isRequestActive) {
                clearTimeout(timeoutId); // Clear timeout if the request completes on time
                setLoading(false);
                setDialogOpen(false);
            }
        }
    }

    const columns = [
        { field: 'Gene', headerName: 'Gene', width: 150 },
        { field: 'Rank', headerName: 'Rank', width: 100 },
        { field: 'Gene ID', headerName: 'Gene ID', width: 150 },
        { field: 'Score', headerName: 'Score', width: 100 },
        { field: 'Status', headerName: 'Status', width: 150 },
    ];

    return (
        <>
            
            <ButtonGroup variant="outlined" aria-label="Basic button group">
                        <Button variant="outlined" onClick={handlePhen2GeneCall} startIcon={<TelegramIcon />} >Call Phen2Gene API</Button>
                        <Button variant="contained" endIcon={<SettingsIcon />} onClick={() => setDialogOpen(true)}>
                        </Button>
                    </ButtonGroup>
            <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
                <DialogTitle>Configuration</DialogTitle>
                <DialogContent>
                    <FormControlLabel
                        control={
                            <Switch
                                checked={includeLowPriority}
                                onChange={(e) => setIncludeLowPriority(e.target.checked)}
                            />
                        }
                        label="Include Low Priority"
                    />
                    <FormControlLabel
                        control={
                            <Switch
                                checked={includePredictedGene}
                                onChange={(e) => setIncludePredictedGene(e.target.checked)}
                            />
                        }
                        label="Include Predicted Gene"
                    />
                    <TextField
                        label="Rank"
                        type="number"
                        value={rank}
                        onChange={(e) => setRank(Number(e.target.value))}
                        fullWidth
                        margin="normal"
                    />
                    <div style={{ marginTop: 20 }}>
                        <label>Threshold (0-1):</label>
                        <Slider
                            value={sliderValue}
                            onChange={(e, newValue) => setSliderValue(newValue)}
                            min={0}
                            max={1}
                            step={0.01}
                        />
                    </div>
                </DialogContent>
            </Dialog>
        
            
        
        </>
    );
};

export default PredictGeneButton;
