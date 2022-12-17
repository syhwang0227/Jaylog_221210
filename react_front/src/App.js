import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Join from 'pages/Join'
import { StoreProvider } from 'stores/RootStore';

const App = () => {
  return (
    <StoreProvider>
      <BrowserRouter>
        <Routes>
          <Route path='/join' element={<Join />} />
        </Routes>
      </BrowserRouter>
    </StoreProvider>

  );
};

export default App