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
import React, { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import toast from "react-hot-toast";

const EditRoomPage = () => {
  const navigate = useNavigate();
  const code = useParams().roomCode;
  const { id } = useSelector((state) => state.user.currentUser);
  const [roomData, setRoomData] = useState({
    id: "",
    is_host: "",
    guest_can_pause: "",
    votes_to_skip: "",
  });
  useEffect(() => {
    fetch(`/api/get-room/?code=${code}&id=${id}`)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log("data to be displayed", data);
        setRoomData({
          id: data?.id,
          is_host: data?.is_host,
          guest_can_pause: data?.guest_can_pause,
          votes_to_skip: data?.votes_to_skip,
        });
      })
      .catch((error) => {
        setError(error);
      });
  }, [code]);

  const handleEditRoom = () => {
    console.log("edit room page", roomData);
    const requestOptions = {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ data: roomData }),
    };
    fetch("/api/edit-room/", requestOptions)
      .then((response) => {
        console.log("first response", response);
        return response.json();
      })
      .then((data) => {
        console.log("second response", data);
        toast.success("Room updated successfully");
        setTimeout(() => {
          navigate(`/room/${code}`);
        }, 4000);
      })
      .catch((error) => {
        console.log("error", error);
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
      {roomData?.is_host && (
        <Paper elevation={4} sx={{ padding: "32px 0px" }}>
          <Grid container rowSpacing={4}>
            <Grid item xs={12} align="center">
              <Typography component="h4" variant="h4">
                Edit Music Room
              </Typography>
            </Grid>
            <Grid item xs={12} align="center">
              <FormControl>
                <FormHelperText>Guest control playback music</FormHelperText>
                <RadioGroup
                  row
                  value={roomData?.guest_can_pause}
                  onClick={(e) =>
                    setRoomData({
                      ...roomData,
                      guest_can_pause: e.target.value,
                    })
                  }
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
                  inputProps={{ min: 1, style: { textAlign: "center" } }}
                  value={roomData?.votes_to_skip}
                  onChange={(e) => {
                    setRoomData({ ...roomData, votes_to_skip: e.target.value });
                  }}
                />
              </FormControl>
            </Grid>
            <Grid item xs={12} align="center">
              <Button
                variant="contained"
                color="primary"
                onClick={handleEditRoom}
              >
                Edit Room
              </Button>
            </Grid>
            <Grid item xs={12} align="center">
              <Button
                component={Link}
                to={`/room/${code}`}
                color="warning"
                variant="contained"
              >
                Back
              </Button>
            </Grid>
          </Grid>
        </Paper>
      )}
    </Box>
  );
};

export default EditRoomPage;
