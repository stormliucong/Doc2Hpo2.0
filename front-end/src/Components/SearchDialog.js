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

const SearchDialog = ({ open, onClose, onConfirm, selectedHighlight }) => {
    const [searchQuery, setSearchQuery] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [selectedItem, setSelectedItem] = useState(null);


    useEffect(() => {
        if (selectedHighlight) {
            console.log('in searchdialog\n', selectedHighlight.selectedText);
            setSearchQuery(selectedHighlight.selectedText); // Populate search box with the selected highlight text
        }
    }, [selectedHighlight]);

    useEffect(() => {
        if (searchQuery) {
            // Placeholder: Replace this with your actual API call.
            fetch(`https://jsonplaceholder.typicode.com/users?q=${searchQuery}`)
                .then((res) => res.json())
                .then((data) => {
                    setSuggestions(data);
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
                                key={item.id}
                                button
                                selected={selectedItem?.id === item.id}
                                onClick={() => handleSelect(item)}
                            >
                                <ListItemText primary={item.name} secondary={item.email} />
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
                                <Typography>Name: {selectedItem.name}</Typography>
                                <Typography>Email: {selectedItem.email}</Typography>
                                <Typography>Username: {selectedItem.username}</Typography>
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
