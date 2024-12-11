import React, { useEffect, useState, useContext } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { DataGrid } from '@mui/x-data-grid';
import { AppContext } from './AppContext';
import PredictGeneButton from './PredictGeneButton';
import { Box } from '@mui/material';

const GeneTable = () => {

    const {genePredictionResults,loading} = useContext(AppContext);

    const columns = [
        { field: 'Gene', headerName: 'Gene', width: 150 },
        { field: 'Rank', headerName: 'Rank', width: 100 },
        { field: 'Gene ID', headerName: 'Gene ID', width: 150 },
        { field: 'Score', headerName: 'Score', width: 100 },
        { field: 'Status', headerName: 'Status', width: 150 },
    ];

    return (
        <>

            <DataGrid rows={genePredictionResults} columns={columns} getRowId={(row) => uuidv4()} loading={loading} />
            <Box
            sx={{
                display: 'flex',
                justifyContent: 'right',
                width: '100%',
                alignItems: 'center',
                gap: 2,
                padding: 2,
            }}
            > <PredictGeneButton /></Box>
        </>
    );
};

export default GeneTable;
            
