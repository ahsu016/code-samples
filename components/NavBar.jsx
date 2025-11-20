import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav style={{ padding: "1rem", backgroundColor: "#eee" }}>
      <Link to="/" style={{ marginRight: "1rem" }}>Home</Link>
      <Link to="/search">Search</Link>
    </nav>
  );
}

export default Navbar;
