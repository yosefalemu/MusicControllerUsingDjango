import React, { useState } from "react";
import { Box, Button, Grid, Paper, TextField, Typography } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";

const LoginPage = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState({
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState({
    email: false,
    password: false,
  });

  const handleFormChange = (event) => {
    const { name, value } = event.target;
    setUser({ ...user, [name]: value });
    setErrors({ ...errors, [name]: false }); // Clear error when typing in the field
  };

  const handleLoginIn = () => {
    let newError = {};
    let hasError = false;
    for (const key in user) {
      if (user[key]?.trim() === "") {
        hasError = true;
        newError[key] = true;
      }
    }
    if (hasError) {
      setErrors(newError);
    } else {
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data: user }),
      };
      fetch("/api/login/", requestOptions)
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          console.log(data);
          if (!data.error) {
            navigate("/");
          }
        })
        .catch((error) => {
          console.log(error);
        });
      console.log("Logging in with:", user);
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
          <Grid item xs={12} align={"center"}>
            <TextField
              required={true}
              type="email"
              variant="standard"
              placeholder="Email"
              name="email"
              value={user.email}
              error={errors.email}
              helperText={errors.email && "Email is required"}
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
              error={errors.password}
              helperText={errors.password && "Password is required"}
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
            <Button component={Link} to="/signup">
              Signup
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default LoginPage;
