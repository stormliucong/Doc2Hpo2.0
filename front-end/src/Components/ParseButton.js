import React, { useContext } from 'react';
import { AppContext } from './AppContext';

import {
    Button
} from '@mui/material';
import TelegramIcon from '@mui/icons-material/Telegram';
import { v4 as uuidv4 } from 'uuid';


const ParseButton = () => {

    const { parseOption, fileText, openaiKey, geminiKey, flaskUrl, setLoading, setError, setHighlights } = useContext(AppContext);

    const handleParse = async () => {
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
            let response;
            if (parseOption === 'Test') {
                response = await fetch(flaskUrl + "/api/hello");
            }
            if (parseOption === 'AC Tree') {
                response = await fetch(flaskUrl + "/api/search/actree", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: fileText })
                });
            }
            if (parseOption === 'SciSpacy') {
                response = await fetch(flaskUrl + "/api/search/scispacy", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: fileText })
                });
            }
            if (parseOption === 'GPT') {
                response = await fetch(flaskUrl + "/api/search/gpt", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: fileText, openaiKey: openaiKey, test: false })
                });
            }

            if (parseOption === 'Gemini') {
                response = await fetch(flaskUrl + "/api/search/gemini", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: fileText, geminiKey: geminiKey })
                });
            }

            // If the request is inactive (timed out), stop processing
            if (!isRequestActive) return;
            // if (!response.ok) throw new Error(`HTTP error! Status: ${JSON.stringify(response)}`);
            if (response.status !== 200) {
                try {
                    const res = await response.json();
                    setError("Error: " + response.status + " " + res.error);
                    return;
                }
                catch (error) {
                    setError("Error: " + response.status + " " + response.statusText);
                    return;
                }
            }
            if (parseOption === 'Test') {
                const res = await response.text();
                setError("This is a Test to " + flaskUrl + "\n" + res.toString());
                return;
            }
            if (parseOption !== 'Test') {
                const res = await response.json();
                // push res into highlights
                const highlights = res.map((r) => {
                    const selectedText = r[2];
                    const start = r[0];
                    const end = r[1];
                    const hpoAttributes = r[3];
                    const priority = hpoAttributes.frequency > 0.05 ? 'Low' : 'Normal';
                    return { id: uuidv4(), selectedText, start, end, hpoAttributes, priority }
                });
                setHighlights(highlights);
            }
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

        <Button Icon={<TelegramIcon />} onClick={handleParse}>{parseOption}</Button>
    );
}

export default ParseButton;
