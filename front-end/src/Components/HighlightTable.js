import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from "@mui/material";

const HighlightTable = ({ highlights }) => {
    return (
      <TableContainer component={Paper} sx={{ mt: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Start</TableCell>
              <TableCell>End</TableCell>
              <TableCell>Substring</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {highlights.map((highlight) => (
              <TableRow key={highlight.id}>
                <TableCell>{highlight.id}</TableCell>
                <TableCell>{highlight.start}</TableCell>
                <TableCell>{highlight.end}</TableCell>
                <TableCell>{highlight.text}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  };

  export default HighlightTable;
