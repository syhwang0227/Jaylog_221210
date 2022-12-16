import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Join from 'pages/Join'

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/join" element={<Join />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App