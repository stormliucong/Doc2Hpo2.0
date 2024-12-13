import React, { useState, useEffect, useContext } from 'react';
import { AppContext } from './AppContext';

import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Box,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Checkbox,
  FormControlLabel,
} from '@mui/material';

function ParseSettings({ open, onClose }) {
  const [selectedOption, setSelectedOption] = useState('option1'); // Default option
  const [showCommonConfig, setShowCommonConfig] = useState(false); // Toggle for common configuration

  const { parseOption, setParseOption, openaiKey, setOpenaiKey, flaskUrl, setFlaskUrl } = useContext(AppContext);

  const handleOptionChange = (event) => {
    setSelectedOption(event.target.value);
    setParseOption(event.target.value);
  };

  useEffect(() => { setSelectedOption(parseOption); }, [parseOption]);

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Settings</DialogTitle>
      <DialogContent>
        {/* Dropdown Menu */}
        <FormControl fullWidth sx={{ marginBottom: 2 }}>
          <InputLabel>Choose an Parser</InputLabel>
          <Select value={selectedOption} onChange={handleOptionChange} label="Choose an Option">
            <MenuItem value="Test">Test</MenuItem>
            {/* Default option */}
            <MenuItem value="AC Tree">AC Tree</MenuItem>
            <MenuItem value="SciSpacy">Scispacy</MenuItem>
            <MenuItem value="GPT">GPT</MenuItem>
          </Select>
        </FormControl>

        {/* Dynamic Configuration Based on Option */}
        {selectedOption === 'Test' && (
          <Box>
            <p>This is a test</p>
          </Box>
        )}

        {selectedOption === 'AC Tree' && (
          <Box>
            <p>Discription of AcTree</p>
          </Box>
        )}

        {selectedOption === 'GPT' && (
          <Box>
            <TextField
              fullWidth
              label="Input Open AI Key here:"
              value={openaiKey}
              onChange={(e) => setOpenaiKey(e.target.value)}
              sx={{ marginBottom: 2 }}
            />
          </Box>
        )}

        {selectedOption === 'SciSpacy' && (
          <Box>
            <p>Description of SciSpacy</p>
          </Box>
        )}

        {/* Common Configuration */}
        <FormControlLabel
          control={
            <Checkbox
              checked={showCommonConfig}
              onChange={(e) => setShowCommonConfig(e.target.checked)}
            />
          }
          label="Show more configurations"
        />
        {showCommonConfig && (
          <Box sx={{ marginTop: 2 }}>
            <TextField
              fullWidth
              label="Backend URL"
              value={flaskUrl}
              onChange={(e) => setFlaskUrl(e.target.value)}
            />
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">
          Cancel
        </Button>
        <Button onClick={onClose} color="primary" variant="contained">
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default ParseSettings;
