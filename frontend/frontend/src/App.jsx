import React, { useState } from "react";
import ProfileList from "./components/ProfileList";
import EditProfile from "./components/EditProfile";
import { Typography, Container, Snackbar, Alert, Box } from "@mui/material";

const App = () => {
  const [selectedProfile, setSelectedProfile] = useState(null);
  const [notification, setNotification] = useState({
    open: false,
    message: "",
    severity: "success",
  });
  const [refreshKey, setRefreshKey] = useState(0); // Aggiunto refreshKey

  const handleSave = () => {
    setSelectedProfile(null);
    showNotification("Profile updated successfully!", "success");
    setRefreshKey((prevKey) => prevKey + 1); // Forza il refresh della lista
  };

  const showNotification = (message, severity) => {
    setNotification({ open: true, message, severity });
  };

  const handleCloseNotification = () => {
    setNotification({ ...notification, open: false });
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography
        variant="h4"
        component="h1"
        sx={{ mb: 4, fontWeight: "bold" }}
      >
        Profile Manager
      </Typography>

      <ProfileList
        onEditProfile={(profile) => setSelectedProfile(profile)}
        refreshKey={refreshKey} // Passa la key come prop
      />

      {selectedProfile && (
        <EditProfile
          profileId={selectedProfile.id}
          initialData={selectedProfile}
          onSave={handleSave}
        />
      )}

      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={handleCloseNotification}
      >
        <Alert
          onClose={handleCloseNotification}
          severity={notification.severity}
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default App;
