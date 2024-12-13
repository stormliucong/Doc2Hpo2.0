import { v4 as uuidv4 } from 'uuid';
import { DataGrid } from '@mui/x-data-grid';
import PredictGene from './PredictGeneButton';
import { AppContext } from './AppContext';
import React, {useContext} from "react";
import { Box, Grid } from "@mui/material";
import PredictGeneButton from "./PredictGeneButton";
import SpeedDial from '@mui/material/SpeedDial';
import SpeedDialAction from '@mui/material/SpeedDialAction';
import SpeedDialIcon from '@mui/material/SpeedDialIcon';
import FileCopyIcon from '@mui/icons-material/FileCopy';
import SaveIcon from '@mui/icons-material/Save';
import PrintIcon from '@mui/icons-material/Print';
import ShareIcon from '@mui/icons-material/Share';
import PostAddIcon from '@mui/icons-material/PostAdd';
import SearchDialog from './SearchDialog';
import Button from '@mui/material/Button';
import DeleteForeverSharpIcon from '@mui/icons-material/DeleteForeverSharp';
import AddIcon from '@mui/icons-material/Add';

const HighlightTable = () => {
  const { highlights, fileText, setHighlights } = useContext(AppContext);
  const [searchDialogOpen, setSearchDialogOpen] = React.useState(false);
  const [selectedHighlight, setSelectedHighlight] = React.useState(null);

  const rows = highlights.map((highlight) => ({
    id: highlight.id,
    selectedText: highlight.selectedText || 'N/A',
    start: highlight.start || 'N/A',
    end: highlight.end || 'N/A',
    priority: highlight.priority || 'N/A',
    hpoName: highlight.hpoAttributes.name || 'No HPO Name',
    hpoId: highlight.hpoAttributes.id || 'No HPO ID',
  }));

  const columns = [
    { field: 'selectedText', headerName: 'Highlighted Text', flex: 2 },
    { field: 'start', headerName: 'Start', flex: 1 },
    { field: 'end', headerName: 'End', flex: 1 },
    { field: 'priority', headerName: 'Priority', flex: 1 },
    { field: 'hpoName', headerName: 'HPO Name', flex: 2 },
    { field: 'hpoId', headerName: 'HPO ID', flex: 2 },
    {
      field: "delete",
      headerName: "Delete",
      renderCell: (params) => (
        <DeleteForeverSharpIcon cursor="pointer"
          onClick={() => handleDelete(params.row.id)}
        >
        </DeleteForeverSharpIcon>
      ),
    },
  ];

  const handleDelete = (id) => {
    setHighlights(highlights.filter((h) => h.id !== id));
  };



  const handleSearchConfirm = (selectedItem) => {
    // add selected selected HPO into highlights
    setHighlights([
      ...highlights,
      { id: Date.now(), selectedText: "manual input", start: -1, end: -1, hpoAttributes: selectedItem, priority: "Normal"}
  ]);
    setSearchDialogOpen(false);
  }

  
    

  return (
    <>
     <Box
                sx={{
                    display: 'flex',
                    justifyContent: 'center',
                    width: '100%',
                    alignItems: 'center',
                    gap: 2,
                    padding: 2,
                }}
            >
              <Button startIcon={<AddIcon />} variant = "outlined" onClick={()=> setSearchDialogOpen(true)}>
          Add a row
        </Button>

            </Box>
   

      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5, 10, 20]}
        disableSelectionOnClick
        autoHeight

      />

      <SearchDialog open={searchDialogOpen} onClose={() => { setSearchDialogOpen(false) }} onConfirm={handleSearchConfirm} selectedHighlight={selectedHighlight} />   
     
      
           
    </>
  );
};

export default HighlightTable;
