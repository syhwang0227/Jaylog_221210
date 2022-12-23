import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Join from 'pages/Join'
import { StoreProvider } from 'stores/RootStore';
import Login from 'pages/Login';
import Posts from 'pages/Posts';
import Post from 'pages/Post';
import InsertPost from 'pages/InsertPost';
import UpdatePost from 'pages/UpdatePost';
import My from 'pages/My';
import ChangeInfo from 'pages/ChangeInfo';
import Error404 from 'pages/Error404';

const App = () => {
  return (
    <StoreProvider>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<Posts />} />
          <Route path='/post/:postIdx' element={<Post />} />           
          <Route path='/join' element={<Join />} />
          <Route path='/login' element={<Login />} />
          <Route path='/insert-post' element={<InsertPost />} />
          <Route path='/update-post/:postIdx' element={<UpdatePost />} />
          <Route path='/my' element={<My />} />
          <Route path='/change-info' element={<ChangeInfo />} />
          <Route path="*" element={<Error404 />} />
        </Routes>
      </BrowserRouter>
    </StoreProvider>

  );
};

export default App