import React, { useContext } from 'react';
import { AppContext } from './AppContext';
import SpeedDial from '@mui/material/SpeedDial';
import SpeedDialAction from '@mui/material/SpeedDialAction';
import SpeedDialIcon from '@mui/material/SpeedDialIcon';
import FileCopyIcon from '@mui/icons-material/FileCopy';
import SaveIcon from '@mui/icons-material/Save';
import RestartAltIcon from '@mui/icons-material/RestartAlt';


const GlobalSpeedDial = () => {

    const { genePredictionResults, highlights, fileText, resetState } = useContext(AppContext);

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
        },
        { icon: <RestartAltIcon onClick={() => resetState()} />, name: 'Reset' },
    ];

    return (
        <>

            <SpeedDial
                ariaLabel="SpeedDial basic example"
                direction="right"
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

        </>
    );
};

export default GlobalSpeedDial;

