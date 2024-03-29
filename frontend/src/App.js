import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import HomePage from "./pages/HomePage";
import JoinRoomPage from "./pages/JoinRoomPage";
import CreateRoomPage from "./pages/CreateRoomPage";
import RoomPage from "./pages/RoomPage";
import EditRoomPage from "./pages/EditRoomPage";
import AlbumsPage from "./pages/AlbumsPage";
import TracksPage from "./pages/TracksPage";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SignUpPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/join" element={<JoinRoomPage />} />
        <Route path="/create" element={<CreateRoomPage />} />
        <Route path="/room/:roomCode" element={<RoomPage />} />
        <Route path="/room/edit/:roomCode" element={<EditRoomPage />} />
        <Route path="/albums/:roomCode" element={<AlbumsPage />} />
        <Route path="/tracks/:roomCode" element={<TracksPage />} />
      </Routes>
    </Router>
  );
};

export default App;
