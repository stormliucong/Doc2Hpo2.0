import React, { useState, useEffect, useContext } from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    TextField, Box, Typography
} from '@mui/material';
import { AppContext } from './AppContext';
import Autocomplete from '@mui/material/Autocomplete';
import CircularProgress from '@mui/material/CircularProgress';

const SearchDialog = ({ open, onClose, onConfirm, selectedHighlight }) => {
    const [searchQuery, setSearchQuery] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [selectedItem, setSelectedItem] = useState(null);
    const { loading, setLoading, error, setError } = useContext(AppContext);



    useEffect(() => {
        if (selectedHighlight) {
            setSearchQuery(selectedHighlight.selectedText); // Populate search box with the selected highlight text
        }
    }, [selectedHighlight]);

    // useEffect(() => {
    //     if (searchQuery) {
    //         setLoading(true);
    //         // https://clinicaltables.nlm.nih.gov/apidoc/hpo/v3/doc.html
    //         fetch(`https://clinicaltables.nlm.nih.gov/api/hpo/v3/search?terms=${searchQuery}`)
    //             .then((res) => res.json())
    //             .then((data) => {
    //                 // reformating the data to match the expected format
    //                 const hpoIdNameList = data[3]
    //                 const hpoIdNameFormatList = hpoIdNameList.map((hpoIdName, index) => ({ id: hpoIdName[0], name: hpoIdName[1] }));
    //                 setSuggestions(hpoIdNameFormatList);
    //             })
    //             .catch((err) => {
    //                 console.error('Error fetching suggestions:', err);
    //                 setSuggestions([]);
    //             });
    //     } else {
    //         setSuggestions([]);
    //         return;
    //     }
    // }, [searchQuery]);

    useEffect(() => {
        if (!searchQuery) {
            setSuggestions([]);
        }

        const fetchOptions = async () => {
            setLoading(true);
            try {
                // Replace with your actual API call
                const response = await fetch(`https://clinicaltables.nlm.nih.gov/api/hpo/v3/search?terms=${searchQuery}`);
                const data = await response.json();

                const hpoIdNameList = data[3]
                const hpoIdNameFormatList = hpoIdNameList.map((hpoIdName, index) => ({ id: hpoIdName[0], name: hpoIdName[1] }));
                // Assume the API returns an array of strings for simplicity
                console.log(hpoIdNameFormatList)
                setSuggestions(hpoIdNameFormatList || []);
            } catch (error) {
                console.error('Error fetching options:', error);
                setError(error);
                setSuggestions([]);
            } finally {
                setLoading(false);
            }
        };

        const debounceTimeout = setTimeout(fetchOptions, 500); // Debounce the API call
        return () => clearTimeout(debounceTimeout); // Cleanup the timeout
    }, [searchQuery]);

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
                <Autocomplete
                    freeSolo // Allows custom input (not limited to options)
                    options={(suggestions)} // Display the name property
                    getOptionLabel={(option) => (option.name ? option.name : '')} // Display the name property
                    isOptionEqualToValue={(option, value) => option.id === value.id} // Match by id
                    loading={loading}
                    inputValue={searchQuery}
                    onInputChange={(event, newInputValue) => {
                        setSearchQuery(newInputValue);
                    }}
                    onChange={(event, newValue) => {
                        setSelectedItem(newValue);
                    }}
                    renderOption={(props, option) => (
                        <Box
                            component="li"
                            {...props}
                            sx={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                padding: '4px 8px',
                            }}
                        >
                            <Typography variant="body1">{option.name}</Typography>
                            <Typography variant="body2" color="text.secondary" sx={{ marginLeft: 1 }}>
                                ({option.id})
                            </Typography>
                        </Box>
                    )}
                    renderInput={(params) => (
                        <TextField
                            {...params}
                            label="Search"
                            variant="outlined"
                            InputProps={{
                                ...params.InputProps,
                                endAdornment: (
                                    <>
                                        {loading ? <CircularProgress color="inherit" size={20} /> : null}
                                        {params.InputProps.endAdornment}
                                    </>
                                ),
                            }}
                        />
                    )}
                />
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
