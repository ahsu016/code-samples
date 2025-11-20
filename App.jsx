import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/NavBar';
import Home from './pages/Home';
import Search from './pages/Search';
import logo from './logo.svg';
import './App.css';

function App() {
  console.log("Rendering App"); // DEBUG LOG
  return (
    <Router>
      <Navbar /> {/* ALWAYS VIS */}

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/search" element={<Search />} />
        <Route
          path="/"
          element={
            <div className="App">
              <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <h1>Welcome to the app!</h1> {/* SIMPLIFIED HEADER */}
                <p>
                  Edit <code>src/App.jsx</code> and save to reload.
                </p>
                <a
                  className="App-link"
                  href="https://reactjs.org"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Learn React
                </a>
              </header>
            </div>
          }
        />
        {/* SEARCH ROUTE */}
        <Route path="/search" element={<Search />} />
      </Routes>
    </Router>
  );
}

export default App;
