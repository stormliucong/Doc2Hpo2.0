import React, { useContext } from 'react';
import { AppContext } from './AppContext';
import { Backdrop, CircularProgress, Snackbar, Alert } from '@mui/material';

const Warnings = () => {
  const { error, setError, loading } = useContext(AppContext);



  return (
    <>
      {/* Error banner using Snackbar and Alert */}

      {error && (
        <Snackbar
          open={Boolean(error)}
          autoHideDuration={60000}
          onClose={() => setError(null)}
          anchorOrigin={{ vertical: "top", horizontal: "center" }}
        >
          <Alert onClose={() => setError(null)} severity="error" sx={{ width: "100%" }}>
            {error}
          </Alert>
        </Snackbar>
      )}

      {/* Full-page backdrop to disable all interactions */}
      <Backdrop
        open={loading}
        style={{
          color: "#fff",
          zIndex: 2000,
          position: "fixed",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
        }}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
    </>
  );
}

export default Warnings;