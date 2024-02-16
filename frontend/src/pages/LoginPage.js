import React from "react";
import { Box, styled } from "@mui/material";

const Container = styled(Box)({
  color: "green",
  cursor: "pointer",
  "&:hover": {
    color: "red",
  },
});

const LoginPage = () => {
  return <Container>Emotion Styled Button</Container>;
};

export default LoginPage;
