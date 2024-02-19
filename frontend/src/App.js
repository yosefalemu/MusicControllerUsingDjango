import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import HomePage from "./pages/HomePage";
import JoinRoomPage from "./pages/JoinRoomPage";
import CreateRoomPage from "./pages/CreateRoomPage";
import RoomPage from "./pages/RoomPage";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/join" element={<JoinRoomPage />} />
        <Route path="/create" element={<CreateRoomPage />} />
        <Route path="/room/:roomCode" element={<RoomPage />} />
      </Routes>
    </Router>
  );
};

export default App;
