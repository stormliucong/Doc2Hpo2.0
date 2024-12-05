import React, { useState, useEffect, useRef } from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    TextField,
    List,
    ListItem,
    ListItemText,
    Box,
    Card,
    CardContent,
    Typography

} from '@mui/material';
import { v4 as uuidv4 } from 'uuid';

const SearchDialog = ({ open, onClose, onConfirm, selectedHighlight }) => {
    const [searchQuery, setSearchQuery] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [selectedItem, setSelectedItem] = useState(null);


    useEffect(() => {
        if (selectedHighlight) {
            setSearchQuery(selectedHighlight.selectedText); // Populate search box with the selected highlight text
        }
    }, [selectedHighlight]);

    useEffect(() => {
        if (searchQuery) {
            // https://clinicaltables.nlm.nih.gov/apidoc/hpo/v3/doc.html
            fetch(`https://clinicaltables.nlm.nih.gov/api/hpo/v3/search?terms=${searchQuery}`)
                .then((res) => res.json())
                .then((data) => {
                    // reformating the data to match the expected format
                    const hpoIdNameList = data[3]
                    const hpoIdNameFormatList = hpoIdNameList.map((hpoIdName, index) => ({ id: hpoIdName[0], name: hpoIdName[1] }));
                    setSuggestions(hpoIdNameFormatList);
                })
                .catch((err) => {
                    console.error('Error fetching suggestions:', err);
                    setSuggestions([]);
                });
        } else {
            setSuggestions([]);
        }
    }, [searchQuery]);

    const handleSelect = (item) => {
        setSelectedItem(item);
    };

    const handleConfirm = () => {
        if (selectedItem) {
            onConfirm(selectedItem);
            setSelectedItem(null);
        }
    };

    return (
        <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
            <DialogTitle>Search</DialogTitle>
            <DialogContent>

                <Box display="flex" alignItems="center"><TextField
                    fullWidth
                    label="Search"
                    variant="outlined"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
                {suggestions &&    <List>
                        {suggestions.map((item) => (
                            <ListItem
                                key={uuidv4()}
                                button
                                selected={selectedItem?.id === item.id}
                                onClick={() => handleSelect(item)}
                            >
                                <ListItemText primary={item.id} secondary={item.name} />
                            </ListItem>
                        ))}
                    </List> 
                }
                {suggestions.length === 0 && <Typography>No suggestions found. Change the search query</Typography>}
                </Box>
                <Box mt={2}>
                    {/* Information Card Section */}
                    {selectedItem && (
                        <Card sx={{ mt: 3 }}>
                            <CardContent>
                                <Typography variant="h6">Selected Item</Typography>
                                <Typography variant="body1">HPO ID: {selectedItem.id}</Typography>
                                <Typography variant="body1">HPO Name: {selectedItem.name}</Typography>
                            </CardContent>
                        </Card>
                    )}
                    {!selectedItem && (
                        <Card sx={{ mt: 3 }}>
                            <CardContent>
                                <Typography variant="h6">No item selected</Typography>
                            </CardContent>
                        </Card>
                    )}
                </Box>

            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Cancel</Button>
                <Button
                    onClick={handleConfirm}
                    color="primary"
                    variant="contained"
                    disabled={!selectedItem}
                >
                    Confirm
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default SearchDialog;
