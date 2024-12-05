import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from "@mui/material";

const HighlightTable = ({ highlights }) => {
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
              
              <TableRow key={highlight.id}>
                <TableCell>{highlight.selectedText}</TableCell>
                <TableCell>{highlight.start}</TableCell>
                <TableCell>{highlight.end}</TableCell>
                <TableCell>{highlight.priority}</TableCell>
                {highlight.hpoAttributes.hpoName && highlight.hpoAttributes.Id ? (
                  <>
                  <TableCell>
                    {highlight.hpoAttributes.hpoName}
                  </TableCell>
                  <TableCell>
                    {highlight.hpoAttributes.hpoId}
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
