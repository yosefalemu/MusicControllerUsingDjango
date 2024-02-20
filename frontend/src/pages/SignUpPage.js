import React, { useState } from "react";
import { Box, Button, Grid, Paper, TextField, Typography } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";
import ClipLoader from "react-spinners/ClipLoader";
import toast from "react-hot-toast";

const SignUpPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState({
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    profile_picture: null,
  });

  const [errors, setErrors] = useState({
    first_name: false,
    last_name: false,
    username: false,
    email: false,
    password: false,
    profile_picture: false,
    passwordMatch: false,
  });

  const handleFormChange = (event) => {
    const { name, value } = event.target;

    setUser({
      ...user,
      [name]: value,
    });

    setErrors({
      ...errors,
      [name]: false,
    });
  };

  const handleImageChange = (event) => {
    const { name } = event.target;
    setUser({ ...user, [name]: event.target.files[0] });
  };

  const handleSignup = async () => {
    const newError = {};
    let hasError = false;

    for (const key in user) {
      if (key === "profile_picture" && user[key] === null) {
        newError[key] = true;
        hasError = true;
      } else if (typeof user[key] === "string" && user[key].trim() === "") {
        newError[key] = true;
        hasError = true;
      }
    }
    if (
      user.password &&
      user.confirmPassword &&
      user.password !== user.confirmPassword
    ) {
      newError.passwordMatch = true;
      hasError = true;
    }

    if (hasError) {
      setErrors(newError);
      return;
    }

    const formData = new FormData();
    for (const key in user) {
      formData.append(key, user[key]);
    }
    const requestOptions = {
      method: "POST",
      body: formData,
    };
    setLoading(true);
    fetch("/api/signup/", requestOptions)
      .then((response) => {
        setLoading(false);
        return response.json();
      })
      .then((data) => {
        setLoading(false);
        if (!data.error) {
          toast.success("User created");
          setTimeout(() => {
            navigate("/home");
          }, 4000);
        } else {
          toast.error(data.error);
          throw new Error();
        }
      })
      .then((error) => {
        setLoading(false);
        console.log(error);
      });
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
            <Typography variant="h4">Sign Up</Typography>
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
              type="text"
              variant="standard"
              placeholder="First Name"
              name="first_name"
              value={user.first_name}
              error={errors.first_name}
              helperText={errors.first_name && "First Name is Required"}
              onChange={handleFormChange}
            />
          </Grid>
          <Grid item xs={12} align={"center"}>
            <TextField
              required={true}
              type="text"
              variant="standard"
              placeholder="Last Name"
              name="last_name"
              value={user.last_name}
              error={errors.last_name}
              helperText={errors.last_name && "Last Name is required"}
              onChange={handleFormChange}
            />
          </Grid>
          <Grid item xs={12} align={"center"}>
            <TextField
              required={true}
              type="text"
              variant="standard"
              placeholder="Username"
              name="username"
              value={user.username}
              error={errors.username}
              helperText={errors.username && "Username is required"}
              onChange={handleFormChange}
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
              error={errors.password || errors.passwordMatch}
              helperText={
                (errors.password && "Password is required") ||
                (errors.passwordMatch && "Password don't match")
              }
              onChange={handleFormChange}
            />
          </Grid>
          <Grid item xs={12} align={"center"}>
            <TextField
              required={true}
              type="password"
              variant="standard"
              placeholder="Confirm password"
              name="confirmPassword"
              value={user.confirmPassword}
              error={errors.confirmPassword || errors.passwordMatch}
              helperText={
                (errors.confirmPassword && "Confirm password is required") ||
                (errors.passwordMatch && "Password don't match")
              }
              onChange={handleFormChange}
            />
          </Grid>
          <Grid item xs={3}></Grid>
          <Grid item xs={6} align={"center"}>
            <TextField
              required={true}
              type="file"
              variant="standard"
              name="profile_picture"
              accept="image/png, image/jpeg"
              error={errors.profile_picture}
              helperText={errors.profile_picture && "Image is required"}
              onChange={handleImageChange}
            />
          </Grid>
          <Grid item xs={12} align={"center"}>
            <Button variant="contained" color="primary" onClick={handleSignup}>
              SignUp
            </Button>
          </Grid>
          <Grid item xs={12} align="center">
            <Typography>Have an account?</Typography>
          </Grid>
          <Grid item xs={12} align="center">
            <Button component={Link} to="/login">
              Login
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default SignUpPage;
