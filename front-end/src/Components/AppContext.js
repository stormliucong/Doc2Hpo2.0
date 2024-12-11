import React, { createContext, useState } from 'react';

export const AppContext = createContext();

export const AppProvider = ({ children }) => {
  // Multiple state variables
  const [fileText, setFileText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleUpdateFileText = (text) => {
    setFileText(text);
  }

  const handleUpdateLoading = (isLoading) => {
    setLoading(isLoading);
  }

  const handleUpdateError = (errorMessage) => {
    setError(errorMessage);
  }


  return (
    <AppContext.Provider value={{ fileText, loading, error, handleUpdateFileText, handleUpdateLoading, handleUpdateError }}>
      {children}
    </AppContext.Provider>
  );
};
