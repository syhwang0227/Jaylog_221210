import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Join from 'pages/Join'
import { StoreProvider } from 'stores/RootStore';
import Login from 'pages/Login';
import Posts from 'pages/Posts';

const App = () => {
  return (
    <StoreProvider>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<Posts />} />
          <Route path='/join' element={<Join />} />
          <Route path='/login' element={<Login />} />
        </Routes>
      </BrowserRouter>
    </StoreProvider>

  );
};

export default App