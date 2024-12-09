import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import GitHubIcon from '@mui/icons-material/GitHub';
import MedicalTextAnnotator from './Components/MedicalTextAnnotator';

// Pages
const Home = () => (
  <Box textAlign="center" mt={4}>
    <Typography variant="h4" component="h1" gutterBottom>
      Welcome to the Doc2Hpo v2.0
    </Typography>
    <Typography variant="subtitle1" color="textSecondary">
      This is the home page of the application.
    </Typography>
    {/* Content Section */}
    <MedicalTextAnnotator />
  </Box>
);

const Features = () => (
  <Box textAlign="center" mt={4}>
    <Typography variant="h4" component="h1" gutterBottom>
      Features
    </Typography>
    <Typography variant="subtitle1" color="textSecondary">
      Explore the features of this app, including text annotation and more.
    </Typography>
  </Box>
);

const Contact = () => (
  <Box textAlign="center" mt={4}>
    <Typography variant="h4" component="h1" gutterBottom>
      Contact Us
    </Typography>
    <Typography variant="subtitle1" color="textSecondary">
      Reach out to us for more information about this app.
    </Typography>
  </Box>
);

const App = () => {
  return (
    <Router>
      <div className="App">
        {/* Navigation Bar */}
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Doc2Hpo v2.0
            </Typography>
            <Button color="inherit" component={Link} to="/">
              Home
            </Button>
            <Button color="inherit" component={Link} to="/features">
              Features
            </Button>
            <Button color="inherit" component={Link} to="/contact">
              Contact
            </Button>
            {/* GitHub Icon */}
            <IconButton
              color="inherit"
              href="https://github.com/stormliucong/doc2hpo"
              target="_blank"
              rel="noopener noreferrer"
            >
              <GitHubIcon />
            </IconButton>
            GitHub
          </Toolbar>
        </AppBar>

        {/* Main Content */}
        <Container maxWidth="lg" sx={{ mt: 4 }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/features" element={<Features />} />
            <Route path="/contact" element={<Contact />} />
          </Routes>
        </Container>

        {/* Footer */}
        <Box
          component="footer"
          sx={{
            py: 2,
            mt: 4,
            backgroundColor: '#f5f5f5',
            textAlign: 'center',
          }}
        >
          <Typography variant="body2" color="textSecondary">
            © {new Date().getFullYear()} Doc2Hpo v2.0. All rights reserved.
          </Typography>
        </Box>
      </div>
    </Router>
  );
};

export default App;
