import { Box, Button, ButtonGroup, Grid, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";

const HomePage = () => {
  const navigate = useNavigate();
  const { id } = useSelector((state) => state.user.currentUser);
  const [userRooms, setUserRooms] = useState({});
  useEffect(() => {
    fetch(`/api/get-user-room/?id=${id}`)
      .then((response) => {
        console.log("first response", response);
        return response.json();
      })
      .then((data) => {
        console.log("second response", data);
      })
      .catch((error) => {
        console.log("error that found", error);
      });
  }, []);
  return (
    <Box
      sx={{
        height: "99%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        border: "2px solid green",
      }}
    >
      <Grid container rowSpacing={3}>
        <Grid item xs={12} align="center">
          <Typography variant="h4">Jossy Room Party</Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <ButtonGroup>
            <Button
              color="primary"
              variant="contained"
              component={Link}
              to="/join"
            >
              Join Room
            </Button>
            <Button
              color="warning"
              variant="contained"
              component={Link}
              to="/create"
            >
              Create Room
            </Button>
          </ButtonGroup>
        </Grid>
        <Grid item xs={12} align="center">
          <Button
            color="error"
            variant="contained"
            component={Link}
            to="/login"
          >
            Logout
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default HomePage;
