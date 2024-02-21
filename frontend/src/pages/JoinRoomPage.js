import React, { useState } from "react";
import { Grid, Typography, Button, TextField, Box, Paper } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";

const JoinRoomPage = () => {
  const navigate = useNavigate();
  const [code, setCode] = useState("");
  const [errorValue, setErrorValue] = useState("");
  const { id } = useSelector((state) => state.user.currentUser);

  const handleClick = () => {
    console.log(code);
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code: code, id: id }),
    };

    console.log(requestOptions.body);
    fetch("/api/join-room/", requestOptions)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log("Responded data", data);
        if (data?.error) {
          throw new Error();
        } else {
          navigate(`/room/${code}`);
        }
      })
      .catch((error) => {
        console.log("log in catch", error);
        setErrorValue(error);
      });
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
      <Paper elevation={4} sx={{ padding: "30px 0px" }}>
        <Grid container rowSpacing={2}>
          <Grid item xs={12} align="center">
            <Typography component={"h4"} variant="h4">
              Join Music Group
            </Typography>
          </Grid>
          <Grid item xs={12} align="center">
            <TextField
              label="code"
              placeholder="Enter the group code"
              variant="standard"
              error={errorValue ? true : false}
              value={code}
              helperText={errorValue.toString()}
              onChange={(e) => setCode(e.target.value)}
            />
          </Grid>
          <Grid item xs={12} align="center">
            <Button variant="contained" color="primary" onClick={handleClick}>
              Enter Room
            </Button>
          </Grid>
          <Grid item xs={12} align="center" component={Link} to={"/home"}>
            <Button variant="contained" color="warning">
              Back
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default JoinRoomPage;
