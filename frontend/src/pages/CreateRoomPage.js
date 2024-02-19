import React, { useState } from "react";
import {
  Box,
  Button,
  FormControl,
  FormControlLabel,
  FormHelperText,
  Grid,
  Paper,
  Radio,
  RadioGroup,
  TextField,
  Typography,
} from "@mui/material";
import { Link, useNavigate } from "react-router-dom";

const CreateRoomPage = () => {
  const navigate = useNavigate();
  const [guest_can_pause, setGuest_can_pause] = useState(true);
  const [votes_to_skip, setVotes_to_skip] = useState(1);
  console.log(votes_to_skip);
  console.log(guest_can_pause);

  const handleButtonClicked = () => {
    const data = { guest_can_pause, votes_to_skip };
    console.log(data);
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ data: data }),
    };
    console.log(requestOptions);
    fetch("/api/create-room/", requestOptions)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Response:", data);
        navigate(`/room/${data.code}`);
      })
      .catch((error) => {
        console.log(error);
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
      <Paper elevation={4} sx={{ padding: "32px 0px" }}>
        <Grid container rowSpacing={4}>
          <Grid item xs={12} align="center">
            <Typography component="h4" variant="h4">
              Create Music Room
            </Typography>
          </Grid>
          <Grid item xs={12} align="center">
            <FormControl>
              <FormHelperText>Guest control playback music</FormHelperText>
              <RadioGroup
                row
                defaultValue={true}
                onChange={(e) => setGuest_can_pause(e.target.value)}
              >
                <FormControlLabel
                  value={true}
                  label="Play/Pause"
                  labelPlacement="bottom"
                  control={<Radio color="primary" />}
                />
                <FormControlLabel
                  value={false}
                  label="No control"
                  labelPlacement="bottom"
                  control={<Radio color="error" />}
                />
              </RadioGroup>
            </FormControl>
          </Grid>
          <Grid item xs={12} align="center">
            <FormControl>
              <FormHelperText>Votes required to skip the song</FormHelperText>
              <TextField
                required={true}
                type="number"
                variant="standard"
                defaultValue={votes_to_skip}
                inputProps={{ min: 1, style: { textAlign: "center" } }}
                onChange={(e) => setVotes_to_skip(e.target.value)}
              />
            </FormControl>
          </Grid>
          <Grid item xs={12} align="center">
            <Button
              variant="contained"
              color="primary"
              onClick={handleButtonClicked}
            >
              Create Room
            </Button>
          </Grid>
          <Grid item xs={12} align="center">
            <Button component={Link} to="/" color="warning" variant="contained">
              Back
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default CreateRoomPage;
