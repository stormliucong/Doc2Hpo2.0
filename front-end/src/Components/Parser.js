import React, { useContext, useState } from 'react';
import { AppContext } from './AppContext';
import { Button } from '@mui/material';
import { v4 as uuidv4 } from 'uuid';
import { Box, Dialog, DialogActions, DialogTitle, TextField } from '@mui/material';

const Parser = () => {
    const { fileText, setHighlights, setHighlightMode, setLoading, setError } = useContext(AppContext);
    const [actreeDialogOpen, setActreeDialogOpen] = useState(false);
    const [gptDialogOpen, setGptDialogOpen] = useState(false);
    const [openaiKey, setOpenaiKey] = useState("");
    const [scispacyDialogOpen, setScispacyDialogOpen] = useState(false);
    


    const testFlask = async () => {
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
            const response = await fetch('http://localhost:5000/api/hello');
            // If the request is inactive (timed out), stop processing
            if (!isRequestActive) return;
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            const res = await response.text();
            alert(res);
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
            }
        }
    }

    const AcTreeFlask = async () => {
        // Post request with {text: fileText}
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
            const response = await fetch('http://localhost:5000/api/search/actree', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: fileText })
            });
            // If the request is inactive (timed out), stop processing
            if (!isRequestActive) return;

            clearTimeout(timeoutId); // Clear timeout if the request completes on time
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            const res = await response.json();
            // push res into highlights
            console.log('flask res', res)
            const highlights = res.map((r) => {
                const selectedText = r[2];
                const start = r[0];
                const end = r[1];
                const hpoAttributes = r[3];
                const priority = hpoAttributes.frequency > 0.05 ? 'Low' : 'Normal';
                return { id: uuidv4(), selectedText, start, end, hpoAttributes, priority }
            });
            setHighlights(highlights);
            setHighlightMode(true);
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
            }
        }
    }

    const GptFlask = async () => {
        // Post request with {text: fileText}
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
            const response = await fetch('http://localhost:5000/api/search/gpt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: fileText, openaiKey: openaiKey, test: false })
            });
            // If the request is inactive (timed out), stop processing
            if (!isRequestActive) return;
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            const res = await response.json();
            // push res into highlights
            console.log('flask res', res)
            const highlights = res.map((r) => {
                const selectedText = r[2];
                const start = r[0];
                const end = r[1];
                const hpoAttributes = r[3];
                const priority = hpoAttributes.frequency > 0.05 ? 'Low' : 'Normal';
                return { id: uuidv4(), selectedText, start, end, hpoAttributes, priority }
            });
            setHighlights(highlights);
            setHighlightMode(true);
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
            }
        }
    }

    const ScispacyFlask = async () => {
        // Post request with {text: fileText}
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
            const response = await fetch('http://localhost:5000/api/search/scispacy', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: fileText })
            });
            // If the request is inactive (timed out), stop processing
            if (!isRequestActive) return;
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            const res = await response.json();
            // push res into highlights
            console.log('flask res', res)
            const highlights = res.map((r) => {
                const selectedText = r[2];
                const start = r[0];
                const end = r[1];
                const hpoAttributes = r[3];
                const priority = hpoAttributes.frequency > 0.05 ? 'Low' : 'Normal';
                return { id: uuidv4(), selectedText, start, end, hpoAttributes, priority }
            });
            setHighlights(highlights);
            setHighlightMode(true);
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
            }
        }
    }


    return (
        <>
            {/* Call Flask ACtree */}
            <Box mb={2}>
                {/* A button to test backend */}
                <Button variant="outlined" component="label" onClick={() => testFlask()}>
                    Test Backend
                </Button>

                <Button variant="outlined" component="label" onClick={() => setActreeDialogOpen(true)}>
                    ACtree Parse
                </Button>
                <Dialog open={actreeDialogOpen} onClose={() => { setActreeDialogOpen(false) }} >
                    <DialogTitle>
                        ACtree Parse Configuration
                    </DialogTitle>
                    <DialogActions>
                        <Button onClick={() => { setActreeDialogOpen(false) }}>Cancel</Button>
                        <Button onClick={() => { setActreeDialogOpen(false); AcTreeFlask() }}>Confirm</Button>
                    </DialogActions>
                </Dialog>

                <Button variant="outlined" component="label" onClick={() => setGptDialogOpen(true)}>
                    GPT Parse
                </Button>
                <Dialog open={gptDialogOpen} onClose={() => { setGptDialogOpen(false); setOpenaiKey('') }} >
                    <DialogTitle>
                        GPT Parse Configuration
                    </DialogTitle>
                    <DialogContent>
                        <TextField
                            fullWidth
                            label="Input OpenAI Key"
                            value={openaiKey}
                            onChange={(e) => setOpenaiKey(e.target.value)}
                        />
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => { setGptDialogOpen(false); setOpenaiKey('') }}>Cancel</Button>
                        <Button onClick={() => { setGptDialogOpen(false); GptFlask() }}>Confirm</Button>
                    </DialogActions>
                </Dialog>

                <Button variant="outlined" component="label" onClick={() => setScispacyDialogOpen(true)}>
                    Scispacy Parse
                </Button>
                <Dialog open={scispacyDialogOpen} onClose={() => { setScispacyDialogOpen(false) }} >
                    <DialogTitle>
                        Scispacy Parse Configuration
                    </DialogTitle>
                    <DialogActions>
                        <Button onClick={() => { setScispacyDialogOpen(false) }}>Cancel</Button>
                        <Button onClick={() => { setScispacyDialogOpen(false); ScispacyFlask() }}>Confirm</Button>
                    </DialogActions>
                </Dialog>
            </Box>
        </>
    );
}

export default Parser;