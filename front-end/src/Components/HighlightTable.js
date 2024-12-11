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
import { Grid2 } from '@mui/material';

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
      field: "actions",
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



  const actions = [
    { icon: <FileCopyIcon onClick = {() => {navigator.clipboard.writeText(JSON.stringify(highlights))}} >

    </FileCopyIcon>, name: 'Copy' },
    { icon: <SaveIcon onClick = {() => {
      const element = document.createElement("a");
      const download_json = { text: fileText, highlights: highlights };
      const file = new Blob([JSON.stringify(download_json)], { type: 'application/json' });
      element.href = URL.createObjectURL(file);
      element.download = "highlights.json";
      document.body.appendChild(element); // Required for this to work in FireFox
      element.click()}}>

      </SaveIcon>, name: 'Save' },
    { icon: <PostAddIcon onClick = {() => {setSearchDialogOpen(true)}}>
    </PostAddIcon>, name: 'Add Hpo' },
      
  ];



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
     
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5, 10, 20]}
        disableSelectionOnClick
        autoHeight
      />
      <SpeedDial
        ariaLabel="SpeedDial basic example"
        icon={<SpeedDialIcon />}
      >
        {actions.map((action) => (
          <SpeedDialAction
            key={action.name}
            icon={action.icon}
            tooltipTitle={action.name}
          />
        ))}
      </SpeedDial> 
      <SearchDialog open={searchDialogOpen} onClose={() => { setSearchDialogOpen(false) }} onConfirm={handleSearchConfirm} selectedHighlight={selectedHighlight} />   
     
      
           
    </>
  );
};

export default HighlightTable;
