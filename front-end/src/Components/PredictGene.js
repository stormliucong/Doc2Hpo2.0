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

const PredictGene = ({ highlights }) => {
    const [dialogOpen, setDialogOpen] = useState(false);
    const [includeLowPriority, setIncludeLowPriority] = useState(false);
    const [includePredictedGene, setIncludePredictedGene] = useState(false);
    const [rank, setRank] = useState(5);
    const [sliderValue, setSliderValue] = useState(0.5);
    const [input, setInput] = useState('');
    const [data, setData] = useState([]);
    const [loading, setLoading, error, setError] = useContext(AppContext);


    useEffect(() => {
        setInput(highlights);
    }, [highlights]);

    const handleDialogOpen = () => setDialogOpen(true);
    const handleDialogClose = () => setDialogOpen(false);

    const handleConfirm = async () => {
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
            <Snackbar
                open={Boolean(error)}
                autoHideDuration={60000}
                onClose={() => setError(null)}
                anchorOrigin={{ vertical: "top", horizontal: "center" }}
            >
                <Alert onClose={() => setError(null)} severity="error" sx={{ width: "100%" }}>
                    {error}
                </Alert>
            </Snackbar>
            {/* Full-page backdrop to disable all interactions */}
            <Backdrop
                open={loading}
                style={{
                    color: "#fff",
                    zIndex: 2000,
                    position: "fixed",
                    top: 0,
                    left: 0,
                    width: "100%",
                    height: "100%",
                }}
            >
                <CircularProgress color="inherit" />
            </Backdrop>
            <Button variant="contained" onClick={handleDialogOpen}>
                Open Configuration
            </Button>

            <Dialog open={dialogOpen} onClose={handleDialogClose}>
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
                <DialogActions>
                    <Button onClick={handleDialogClose}>Cancel</Button>
                    <Button onClick={handleConfirm} variant="contained">
                        Confirm
                    </Button>
                </DialogActions>
            </Dialog>
        {data.length > 0 && 
            <div style={{ marginTop: 20, height: 400 }}>
                <DataGrid rows={data} columns={columns} getRowId={(row) => uuidv4()} loading={loading} />
            </div>
        }
        </>
    );
};

export default PredictGene;
