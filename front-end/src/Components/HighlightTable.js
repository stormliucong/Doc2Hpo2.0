import { v4 as uuidv4 } from 'uuid';
import { DataGrid } from '@mui/x-data-grid';
import PredictGene from './PredictGene';
import { AppContext } from './AppContext';
import React, {useContext} from "react";


const HighlightTable = () => {
  const { highlights } = useContext(AppContext);


  if (!highlights || highlights.length === 0) {
    return <p>No highlights available.</p>; // Replace with a suitable message or UI.
  }
  const rows = highlights.map((highlight) => ({
    id: uuidv4(), // Unique identifier for each row
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
  ];

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
      {/* <PredictGene highlights={highlights} /> */}
    </>
  );
};

  export default HighlightTable;
