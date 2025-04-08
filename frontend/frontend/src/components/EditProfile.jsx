import React, { useState } from "react";
import axios from "axios";
import {
  TextField,
  Button,
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
} from "@mui/material";

const EditProfile = ({ profileId, initialData, onSave }) => {
  const [formData, setFormData] = useState(initialData);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.put(
        `http://localhost:8080/api/v1/profiles/${profileId}`,
        formData
      );
      onSave();
    } catch (error) {
      console.error("Update error:", error.response || error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open onClose={onSave} fullWidth maxWidth="sm">
      <DialogTitle>Edit Profile</DialogTitle>
      <DialogContent>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
          <TextField
            name="name"
            label="Name"
            value={formData.name}
            onChange={handleChange}
            fullWidth
            margin="normal"
            required
          />
          <TextField
            name="surname"
            label="Surname"
            value={formData.surname}
            onChange={handleChange}
            fullWidth
            margin="normal"
            required
          />
          <TextField
            name="codiceFiscale"
            label="Codice Fiscale"
            value={formData.codiceFiscale || ""}
            onChange={handleChange}
            fullWidth
            margin="normal"
          />
          <TextField
            name="birthDate"
            label="Birth Date"
            type="date"
            InputLabelProps={{ shrink: true }}
            value={formData.birthDate.split("T")[0] || ""}
            onChange={handleChange}
            fullWidth
            margin="normal"
            required
          />
          <TextField
            name="sex"
            label="Sex (M/F)"
            value={formData.sex}
            onChange={handleChange}
            fullWidth
            margin="normal"
            required
          />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onSave}>Cancel</Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          color="primary"
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : "Save Changes"}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default EditProfile;
