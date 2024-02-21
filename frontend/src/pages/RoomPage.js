import { Box, Paper, Typography, Grid, Button } from "@mui/material";
import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { useSelector } from "react-redux";

const RoomPage = () => {
  const code = useParams().roomCode;
  const { id } = useSelector((state) => state.user.currentUser);
  const [error, setError] = useState("");
  const [roomData, setRoomData] = useState(null);

  console.log("user id in ger room", id);

  useEffect(() => {
    fetch(`/api/get-room/?code=${code}&id=${id}`)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log("data to be displayed", data);
        setRoomData(data);
      })
      .catch((error) => {
        setError(error);
      });
  }, [code]);

  const handleLeaveRoom = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        is_host: roomData?.is_host,
        room_id: roomData?.id,
        user_id: id,
      }),
    };
    console.log(requestOptions.body);
    fetch("/api/remove-user-from-room/", requestOptions)
      .then((response) => {
        console.log("first response", response);
        return response.json();
      })
      .then((data) => {
        console.log("second response", data);
      })
      .catch((error) => {
        console.log("error occured", error);
      });
    console.log("button clicked");
  };

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
      <Paper
        elevation={4}
        sx={{
          display: "flex",
          flexDirection: "column",
          gap: "20px",
          padding: "30px 20px",
          width: "30%",
          border: "2px solid red",
        }}
      >
        <Grid container rowSpacing={2}>
          <Grid item xs={6}>
            <Typography> Code</Typography>
          </Grid>
          <Grid item xs={6} align="center">
            <Typography>{roomData?.code}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography>Guest Can Pause</Typography>
          </Grid>
          <Grid item xs={6} align="center">
            <Typography>{roomData?.guest_can_pause.toString()}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography>Host</Typography>
          </Grid>
          <Grid item xs={6} align="center">
            <Typography>{roomData?.host}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography>Is Host</Typography>
          </Grid>
          <Grid item xs={6} align="center">
            <Typography>{roomData?.is_host.toString()}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography>Votes To Skip</Typography>
          </Grid>
          <Grid item xs={6} align="center">
            <Typography>{roomData?.votes_to_skip}</Typography>
          </Grid>
          <Grid item xs={12} align="center">
            <Button
              color="warning"
              variant="contained"
              onClick={handleLeaveRoom}
            >
              Leave Room
            </Button>
          </Grid>
          {roomData?.is_host && (
            <Grid item xs={12} align="center">
              <Button
                color="warning"
                variant="contained"
                component={Link}
                to={`/room/edit/${code}`}
              >
                Edit Room
              </Button>
            </Grid>
          )}
          <Grid item xs={12} align="center">
            <Button
              color="primary"
              variant="contained"
              component={Link}
              to="/home"
            >
              Back
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default RoomPage;
