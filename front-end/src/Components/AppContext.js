import React, { createContext, useState } from 'react';

const AppContext = createContext();

const AppProvider = ({ children }) => {
  // Multiple state variables
  const [fileText, setFileText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [highlights, setHighlights] = useState([]);
  const [highlightMode, setHighlightMode] = useState(false);
  const [selectedHighlight, setSelectedHighlight] = useState(null);
  const [gptDialogOpen, setGptDialogOpen] = useState(false);
  const [openaiKey, setOpenaiKey] = useState("");
  const [scispacyDialogOpen, setScispacyDialogOpen] = useState(false);
  const [actreeDialogOpen, setActreeDialogOpen] = useState(false);




  return (
    <AppContext.Provider value={{ fileText, setFileText, loading, setLoading, error, setError, highlights, setHighlights, highlightMode, setHighlightMode, selectedHighlight, setSelectedHighlight, gptDialogOpen, setGptDialogOpen, openaiKey, setOpenaiKey, scispacyDialogOpen, setScispacyDialogOpen, actreeDialogOpen, setActreeDialogOpen }}>
      {children}
    </AppContext.Provider>
  );
};

export { AppContext }; // Export AppContext if needed

export default AppProvider; // Default export

