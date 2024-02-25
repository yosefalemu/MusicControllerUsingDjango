import React, { useState } from "react";
import { Box, Button, Grid, Paper, TextField, Typography } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { loginUserSuccess } from "../redux/slices/userSlice";
import ClipLoader from "react-spinners/ClipLoader";
import toast from "react-hot-toast";

const LoginPage = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState({
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState({
    email: "",
    password: "",
  });

  const handleFormChange = (event) => {
    const { name, value } = event.target;
    setUser({ ...user, [name]: value });
    setErrors({ ...errors, [name]: "" });
  };

  const handleLoginIn = () => {
    let newError = {};
    let hasError = false;
    for (const key in user) {
      if (user[key]?.trim() === "") {
        hasError = true;
        newError[key] = `${key} is required`;
      }
    }
    if (hasError) {
      setErrors(newError);
      return;
    } else {
      setLoading(true);
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data: user }),
      };
      fetch("/api/login/", requestOptions)
        .then((response) => {
          setLoading(false);
          if (response.ok) {
            return response.json();
          } else {
            return response.json().then((error) => {
              console.log("Error", error);
              if (error.email) {
                setErrors({ email: error.email });
                throw new Error();
              } else if (error.password) {
                setErrors({ password: error.password });
                throw new Error();
              } else {
                toast.error("Something went wrong");
                throw new Error();
              }
            });
          }
        })
        .then((data) => {
          setLoading(false);
          const data_to_dispatch = { ...data.user, ...data.custom_user };
          dispatch(loginUserSuccess(data_to_dispatch));
          toast.success("Logged in");
          setTimeout(() => {
            navigate("/home");
          }, 4000);
        })
        .catch((error) => {
          setLoading(false);
          console.log("error found", error);
        });
    }
  };

  return (
    <Box
      elevation={4}
      sx={{
        minHeight: "99%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        border: "2px solid green",
        padding: "50px",
      }}
    >
      <Paper elevation={4} sx={{ width: "40%", padding: "30px 10px" }}>
        <Grid container rowSpacing={3}>
          <Grid item xs={12} align="center">
            <Typography variant="h4">Login</Typography>
          </Grid>
          <Grid item xs={12} align="center">
            <ClipLoader
              color={"#36d7b7"}
              loading={loading}
              size={50}
              aria-label="Loading Spinner"
              data-testid="loader"
            />
          </Grid>
          <Grid item xs={12} align={"center"}>
            <TextField
              required={true}
              type="email"
              variant="standard"
              placeholder="Email"
              name="email"
              value={user.email}
              error={!!errors.email}
              helperText={errors.email}
              onChange={handleFormChange}
            />
          </Grid>
          <Grid item xs={12} align={"center"}>
            <TextField
              required={true}
              type="password"
              variant="standard"
              placeholder="Password"
              name="password"
              value={user.password}
              error={!!errors.password}
              helperText={errors.password}
              onChange={handleFormChange}
            />
          </Grid>
          <Grid item xs={12} align={"center"}>
            <Button variant="contained" color="primary" onClick={handleLoginIn}>
              Login
            </Button>
          </Grid>
          <Grid item xs={12} align="center">
            <Typography>Dont have an account?</Typography>
          </Grid>
          <Grid item xs={12} align="center">
            <Button component={Link} to="/">
              Signup
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default LoginPage;
