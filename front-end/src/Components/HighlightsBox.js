import React, { useContext, useEffect, useState } from 'react';
import { AppContext } from './AppContext';
import { v4 as uuidv4 } from 'uuid';
import { Box, Button, FormGroup, FormControlLabel, Switch, Typography, Grid2 } from '@mui/material';
import HighlightButton from './HighlightButton';
import SearchDialog from './SearchDialog';




const HighlightsBox = () => {
    const { setError, setFileText, selectedHighlight, setSelectedHighlight, highlightMode, setHighlightMode, highlights, setHighlights, fileText, inputText } = useContext(AppContext);
    const [dialogOpen, setDialogOpen] = useState(false);

    useEffect(() => {
        if (inputText) {
            setHighlightMode(false);
            setHighlights([]);
            setSelectedHighlight(null);
            setFileText(inputText);
        }
    }, [inputText]);

    const handleHighlight = () => {
        const selection = window.getSelection();
        if (selection && selection.toString().trim() && highlightMode) {
            const selectedText = selection.toString();

            // Ensure we use the specific container for the entire text
            const container = document.getElementById("text-container");    

            const range = selection.getRangeAt(0); // Get the selected range
            const preCaretRange = document.createRange();

            // Set the range to include everything up to the selection
            preCaretRange.setStart(container, 0);
            preCaretRange.setEnd(range.startContainer, range.startOffset);

            // Calculate start and end offsets based on text only
            const start = preCaretRange.toString().length; // Length of text before the selection
            const end = start + range.toString().length; // Add the selected text length

            alert(`Start: ${start}, End: ${end}`);

            // Check if this range is already highlighted
            if (
                highlights.some(
                    (highlight) =>
                        (start >= highlight.start && start < highlight.end) ||
                        (end > highlight.start && end <= highlight.end) || 
                        (highlight.start >= start && highlight.start < end) ||
                        (highlight.end > start && highlight.end <= end)
                )
            ) {
                alert("This text overlaps an existing highlight.");
                selection.removeAllRanges();
                return;
            }

            const hpoAttributes = {};
            const priority = 'Normal';

            setHighlights([
                ...highlights,
                { id: Date.now(), selectedText, start, end, hpoAttributes, priority },
            ]);
            selection.removeAllRanges(); // Clear selection after highlighting
        }
    };

    const handleDeleteHighlight = (selectedHighlight) => {
        if (!highlightMode) return;
        setHighlights(highlights.filter((h) => h.id !== selectedHighlight.id));

    };

    const handleUpdateHighlight = (updatedHighlight) => {
        if (!highlightMode) return;
        setHighlights((prevHighlights) =>
            prevHighlights.map((h) =>
                h.id === updatedHighlight.id ? updatedHighlight : h
            )
        );
    };

    const handleClickHighlight = (selectedHighlight) => {
        if (!highlightMode) return;
        setSelectedHighlight(selectedHighlight);
        setDialogOpen(true);
      };

    const renderHighlightedText = () => {
        if (!fileText) return "Text will appear here...";

        let offset = 0;
        // clear the text container
        return (
            <>
                {highlights
                    .sort((a, b) => a.start - b.start)
                    .reduce((acc, highlight) => {
                        const beforeHighlight = fileText.slice(offset, highlight.start);
                        const highlightedText = fileText.slice(highlight.start, highlight.end);
                        offset = highlight.end;

                        acc.push(<span key={`before-${highlight.id}`}>{beforeHighlight}</span>);

                        acc.push(
                            <HighlightButton
                                key={uuidv4()}
                                highlight={highlight}
                                highlightedText={highlightedText}
                                onUpdateHighlight={handleUpdateHighlight}
                                onDeleteHighlight={handleDeleteHighlight}
                                onClickHighlight={handleClickHighlight}
                            />
                        );

                        return acc;
                    }, [])}
                <span>{fileText.slice(offset)}</span>
            </>
        );
    };

    
      const handleSearchConfirm = (hpo) => {
        console.log('handleConfirm', hpo)
        const updatedHighlight = { ...selectedHighlight, hpoAttributes: hpo };
        handleUpdateHighlight(updatedHighlight);
        setDialogOpen(false);
      };

    return (
        <>
            {/* Annotation region */}
          {/* Toggle Switch */}
          <Grid2 container spacing={2} size={12}>
          <FormGroup>
            <FormControlLabel
              control={
                <Switch
                  checked={highlightMode}
                  onChange={(e) => setHighlightMode(e.target.checked)}
                />
              }
              label="Highlight Mode"
            />
            {/* a download button to download highlights as a json file */}
            <Button variant="outlined" onClick={() => {
              const element = document.createElement("a");
              const download_json = { text: fileText, highlights: highlights };
              const file = new Blob([JSON.stringify(download_json)], { type: 'application/json' });
              element.href = URL.createObjectURL(file);
              element.download = "highlights.json";
              document.body.appendChild(element); // Required for this to work in FireFox
              element.click();
            }
            }>
              Download Highlights
            </Button>
        

          </FormGroup>
            
            
            {/* Add a color legend for Priority and Normal Not clickable button*/}
            <Typography>Priority:</Typography>
            <Button variant="contained" style={{ backgroundColor: "#FFC107", color: "#FFFFFF", padding: "0 5px", margin: "0 2px", borderRadius: "4px", fontSize: "inherit", textTransform: "none", cursor: "pointer", }} size="small">Normal</Button>
            <Button variant="contained" style={{ backgroundColor: "#FF5722", color: "#FFFFFF", padding: "0 5px", margin: "0 2px", borderRadius: "4px", fontSize: "inherit", textTransform: "none", cursor: "pointer", }} size="small">High</Button>
        </Grid2>
        <Grid2 container spacing={2} size={12}>
            <Box
            sx={{width: '100%',         // Matches the `fullWidth` of the TextField
                height: 12 * 24 + 16,  // 12 rows of text with a line height of 24px, plus padding
                padding: 2,            // Padding similar to the TextField's spacing
                border: '1px solid gray',
                borderRadius: 1,       // Border radius for styling
                overflow: 'auto',      // Add scroll for large content
                backgroundColor: 'white',
                textAlign: 'left',       // Aligns text to the left
                whiteSpace: 'pre-wrap', // Preserve line breaks and spaces
                fontFamily: "Merriweather Georgia serif", // Matches TextField font
                fontSize: '1rem',      // Matches TextField text size
                lineHeight: '1.5',     // Matches TextField line spacing
              }}
                id="text-container"
                onMouseUp={handleHighlight}
                style={{ cursor: highlightMode ? "text" : "default" }}
            >
                {renderHighlightedText()}
            </Box>
            <SearchDialog open={dialogOpen} onClose={()=>{setDialogOpen(false)}} onConfirm={handleSearchConfirm} selectedHighlight={selectedHighlight} />
        </Grid2>
        </>
    );
}

export default HighlightsBox;