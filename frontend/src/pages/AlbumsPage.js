import {
  Box,
  Button,
  Grid,
  Pagination,
  TextField,
  Typography,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import React, { useState, useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";

const AlbumsPage = () => {
  const { roomCode } = useParams();
  const [artistName, setArtistName] = useState("");
  const [albums, setAlbums] = useState([]);
  const [hoveredItem, setHoveredItem] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const albumsPerPage = 5;

  useEffect(() => {
    fetch(`/spotify/get-several-album/?artistName=${artistName}`)
      .then((response) => {
        console.log("first response", response);
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Network response was not ok");
        }
      })
      .then((data) => {
        console.log("second response", data);
        setAlbums(data.albums || []);
      })
      .catch((error) => {
        console.error("Error response", error);
      });
  }, [artistName]);

  const handlePageChange = (event, value) => {
    setCurrentPage(value);
  };

  console.log("all albums", albums?.length);
  const total_number_of_pages = Math.ceil(albums?.length / 10);
  console.log("total number of pages", total_number_of_pages);

  const startIndex = (currentPage - 1) * albumsPerPage;
  const endIndex = startIndex + albumsPerPage;
  const currentDisplayedAlbums = albums.slice(startIndex, endIndex);

  return (
    <Box padding={10}>
      <Grid
        container
        sx={{ border: "1px solid red" }}
        justifyContent={"center"}
        alignItems={"center"}
        padding={4}
        rowGap={4}
      >
        <Grid item xs={8}>
          <Box
            sx={{
              display: "flex",
              alignItems: "flex-end",
              border: "2px solid green",
              justifyContent: "center",
            }}
          >
            <SearchIcon sx={{ color: "action.active", mr: 1, my: 0.5 }} />
            <TextField
              id="input-with-sx"
              label="Search album"
              variant="standard"
              onChange={(e) => setArtistName(e.target.value)}
            />
          </Box>
        </Grid>
        <Grid
          container
          item
          xs={8}
          sx={{ border: "1px solid red" }}
          justifyContent={"left"}
          alignItems={"center"}
          rowGap={3}
        >
          <Grid item xs={8}>
            {total_number_of_pages > 0 && (
              <Pagination
                count={total_number_of_pages}
                page={currentPage}
                variant="outlined"
                shape="rounded"
                onChange={handlePageChange}
              />
            )}
          </Grid>
          <Grid item xs={12} sx={{ border: "1px solid red" }}>
            {currentDisplayedAlbums?.map((item, index) => {
              return (
                <Grid
                  container
                  key={item?.id}
                  marginBottom={3}
                  alignItems={"center"}
                  sx={{
                    background: "gray",
                    borderRadius: "10px",
                    padding: "20px",
                    position: "relative",
                  }}
                  onMouseEnter={() => setHoveredItem(index)}
                  onMouseLeave={() => setHoveredItem(null)}
                >
                  <Grid item xs={4}>
                    <img
                      src={item?.images[1]?.url || "placeholder-url"}
                      style={{
                        borderRadius: "50%",
                        objectFit: "cover",
                        width: "150px",
                        height: "150px",
                      }}
                    />
                  </Grid>
                  <Grid item xs={8}>
                    <Typography variant="h1" color={"#fff"} fontSize={"32px"}>
                      {item?.name.length > 30
                        ? `${item.name.slice(0, 30)}...`
                        : item.name}
                    </Typography>
                    <Typography variant="h3" color={"#fff"} fontSize={"24px"}>
                      {item?.artists[0].name}
                    </Typography>
                    <Typography
                      variant="h6"
                      color={"#fff"}
                      fontSize={"18px"}
                    >{`${item?.total_tracks} Tracks`}</Typography>
                  </Grid>
                  {hoveredItem === index && (
                    <Box
                      sx={{
                        position: "absolute",
                        top: "10px",
                        right: "10px",
                        background: "green",
                        borderRadius: "50%",
                        padding: "10px",
                        height: "30px",
                        width: "30px",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                      }}
                    >
                      <PlayArrowIcon style={{ fontSize: 40, color: "white" }} />
                    </Box>
                  )}
                </Grid>
              );
            })}
          </Grid>
          <Grid item xs={4}>
            <Button
              component={Link}
              to={`/room/${roomCode}`}
              variant="contained"
              color="primary"
              fullWidth
            >
              Back
            </Button>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AlbumsPage;
