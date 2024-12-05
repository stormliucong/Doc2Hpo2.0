import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from "@mui/material";
import { v4 as uuidv4 } from 'uuid';

const HighlightTable = ({ highlights }) => {
  console.log('highlight table', highlights)
    return (
      <TableContainer component={Paper} sx={{ mt: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Highlighted Text</TableCell>
              <TableCell>Start</TableCell>
              <TableCell>End</TableCell>
              <TableCell>Priority</TableCell>
              <TableCell>HPO Name</TableCell>
              <TableCell>HPO ID</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {highlights.map((highlight) => (
              
              <TableRow key={uuidv4()}>
                <TableCell>{highlight.selectedText}</TableCell>
                <TableCell>{highlight.start}</TableCell>
                <TableCell>{highlight.end}</TableCell>
                <TableCell>{highlight.priority}</TableCell>
                {highlight.hpoAttributes.name && highlight.hpoAttributes.id ? (
                  <>
                  <TableCell>
                    {highlight.hpoAttributes.name}
                  </TableCell>
                  <TableCell>
                    {highlight.hpoAttributes.id}
                  </TableCell>
                  </>
                ) : (
                  <>
                  <TableCell>No HPO Name</TableCell>
                  <TableCell>No HPO ID</TableCell>
                  </>
                )}
                </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  };

  export default HighlightTable;
