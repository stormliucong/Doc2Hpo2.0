import React, { useEffect, useState, useContext } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { DataGrid } from '@mui/x-data-grid';
import { AppContext } from './AppContext';
import PredictGeneButton from './PredictGeneButton';
import { Box } from '@mui/material';
import SpeedDial from '@mui/material/SpeedDial';
import SpeedDialAction from '@mui/material/SpeedDialAction';
import SpeedDialIcon from '@mui/material/SpeedDialIcon';
import FileCopyIcon from '@mui/icons-material/FileCopy';
import SaveIcon from '@mui/icons-material/Save';


const GeneTable = () => {

    const { genePredictionResults, loading, highlights, fileText } = useContext(AppContext);

    const columns = [
        { field: 'Gene', headerName: 'Gene', width: 150 },
        { field: 'Rank', headerName: 'Rank', width: 100 },
        { field: 'Gene ID', headerName: 'Gene ID', width: 150 },
        { field: 'Score', headerName: 'Score', width: 100 },
        { field: 'Status', headerName: 'Status', width: 150 },
    ];

    const actions = [
        {
            icon: <FileCopyIcon onClick={() => { navigator.clipboard.writeText(JSON.stringify({ text: fileText, highlights: highlights, genePredictionResults: genePredictionResults })) }} >

            </FileCopyIcon>, name: 'Copy'
        },
        {
            icon: <SaveIcon onClick={() => {
                const element = document.createElement("a");
                const download_json = { text: fileText, highlights: highlights, genePredictionResults: genePredictionResults };
                const file = new Blob([JSON.stringify(download_json)], { type: 'application/json' });
                element.href = URL.createObjectURL(file);
                element.download = "gene_prediction_results.json";
                document.body.appendChild(element); // Required for this to work in FireFox
                element.click()
            }}>

            </SaveIcon>, name: 'Save'
        }
    ];

    return (
        <>

            <DataGrid rows={genePredictionResults} columns={columns} pageSize={5} 
            getRowId={(row) => uuidv4()}
                rowsPerPageOptions={[5, 10, 20]}
                disableSelectionOnClick
                autoHeight />
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

            <Box
                sx={{
                    display: 'flex',
                    justifyContent: 'right',
                    width: '100%',
                    alignItems: 'center',
                    gap: 2,
                    padding: 2,
                }}
            >

                <PredictGeneButton /></Box>
        </>
    );
};

export default GeneTable;

