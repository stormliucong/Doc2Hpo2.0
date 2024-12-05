import React, { useState } from "react";
import {
  Box,
  Button,
  TextField,
  Switch,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  List,
  ListItem,
  Typography,
  FormGroup,
  FormControlLabel
} from "@mui/material";
import HighlightTable from "./HighlightTable";
import HighlightButton from "./HighlightButton";
import SearchDialog from "./SearchDialog";

const MedicalTextAnnotator = () => {
  const [inputText, setInputText] = useState("");
  const [fileText, setFileText] = useState("");
  const [highlightMode, setHighlightMode] = useState(false);
  const [highlights, setHighlights] = useState([]);
  const [selectedHighlight, setSelectedHighlight] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);


  const resetState = () => {
    setInputText("");
    setFileText("");
    setHighlightMode(false);
    setHighlights([]);
    setSelectedHighlight(null);
    setDialogOpen(false);
  };
  
  const handleTextSubmit = () => {
    resetState();
    setFileText(inputText);
  }

  const handleFileUpload = (event) => {
    resetState();
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => setFileText(e.target.result);
    reader.readAsText(file);
  };

  const loadPatientTxt = async (file) => {
    // Load the patient text from the public folder using require
    resetState();
    console.log(file)
    try {

      const response = await fetch(file);
      if (!response.ok) throw new Error("Failed to fetch file");
      const text = await response.text();
      setFileText(text);
    } catch (error) {
      console.error(error);
      setFileText("");
    }
  }
    
    

  const handleHighlight = () => {
    const selection = window.getSelection();
    if (selection && selection.toString().trim() && highlightMode) {
      const range = selection.getRangeAt(0);
      const selectedText = selection.toString();

      // Ensure we use the specific container for the entire text
      const container = document.getElementById("text-container");

      if (!container.contains(range.commonAncestorContainer)) {
        alert("Please select text within the specified container.");
        selection.removeAllRanges();
        return;
      }

      // Calculate absolute start and end indices based on the entire text
      const textContent = container.textContent;
      const start = textContent.indexOf(selectedText, range.startOffset);
      const end = start + selectedText.length;
      console.log(container.textContent, start, end);

      // Check if this range is already highlighted
      if (
        highlights.some(
          (highlight) =>
            (start >= highlight.start && start < highlight.end) ||
            (end > highlight.start && end <= highlight.end)
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
        { id: Date.now(), selectedText, start, end, hpoAttributes, priority},
      ]);
      selection.removeAllRanges(); // Clear selection after highlighting
    }
  };

  const handleClickHighlight = (selectedHighlight) => {
    setSelectedHighlight(selectedHighlight);
    setDialogOpen(true);
  };

  const handleDeleteHighlight = (selectedHighlight) => {
    console.log('handleDeleteHighlight')
    console.log(selectedHighlight)

    setHighlights(highlights.filter((h) => h.id !== selectedHighlight.id));
    
  };

  const handleUpdateHighlight = (updatedHighlight) => {
    setHighlights((prevHighlights) =>
      prevHighlights.map((h) =>
        h.id === updatedHighlight.id ? updatedHighlight : h
      )
    );
  };

  const renderHighlightedText = () => {
    if (!fileText) return "Text will appear here...";
  
    let offset = 0;
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
                key={highlight.id}
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
  
  const handleOpenDialog = () => {
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
  };

  const handleConfirm = (hpo) => {
    console.log('handleConfirm', hpo)
    const updatedHighlight = { ...selectedHighlight, hpoAttributes: hpo };
    handleUpdateHighlight(updatedHighlight);
    setDialogOpen(false);
  };

  const testFlask = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/hello');
      if (!response.ok) throw new Error("Failed to fetch file");
      const res = await response.text();
      alert(res);
    }
    catch (error) {
      alert(error);
    }
  }

  return (
    <Box p={2}>
      <Box mb={2}>
        <TextField
          fullWidth
          label="Input Text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />

        <Button variant="contained" onClick={handleTextSubmit} sx={{ mt: 1 }}>
          Submit
        </Button>
      </Box>

      <Box mb={2}>
        <Button variant="outlined" component="label">
          Upload File
          <input type="file" hidden onChange={handleFileUpload} />
        </Button>
      </Box>

      <Box mb={2}>
        <Button variant="outlined" component="label" onClick={() => loadPatientTxt('./demo_patient_1.txt')}>  
          Load Demo Patient 1
        </Button>
      </Box>

      {/* A button to test backend */}
      <Box mb={2}>
        <Button variant="outlined" component="label" onClick={() => testFlask()}>
          Test Backend
        </Button>
      </Box>



      <HighlightTable highlights={highlights} />

      {/* Annotation region */}
      <Box
        id="text-container"
        p={2}
        border={1}
        onMouseUp={handleHighlight}
        style={{ cursor: highlightMode ? "text" : "default" }}
      >
        {renderHighlightedText()}
      </Box>

      {/* Configuration and explanation */}
      <Box mt={2}>
        {/* Toggle Switch */}
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
          
        </FormGroup>
        
      </Box>

      {/* Add a color legend for Priority and Normal Not clickable button*/}
      <Box mt={2}>
        <Typography>Priority:</Typography>
        <Button variant="contained" style={{ backgroundColor: "#FFC107", color: "#FFFFFF", padding: "0 5px", margin: "0 2px", borderRadius: "4px", fontSize: "inherit", textTransform: "none", cursor: "pointer", }} size="small">Normal</Button>
        <Button variant="contained" style={{ backgroundColor: "#FF5722", color: "#FFFFFF", padding: "0 5px", margin: "0 2px", borderRadius: "4px", fontSize: "inherit", textTransform: "none", cursor: "pointer", }} size="small">High</Button>
      </Box>

      <SearchDialog open={dialogOpen} onClose={handleCloseDialog} onConfirm={handleConfirm} selectedHighlight={selectedHighlight} />
      
    </Box>
  );
};

export default MedicalTextAnnotator;
