const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const userRoutes = require('./routes/users');
const spotifyRoutes = require('./routes/spotify');
const auth = require('./middleware/auth');

const app = express();

// Middleware
app.use(express.json());
app.use(cors());

// MongoDB Connection
mongoose.connect('mongodb://localhost/music-app', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
}).then(() => console.log('Connected to MongoDB'));

// Routes
app.use('/api/users', userRoutes);
app.use('/api/spotify', auth, spotifyRoutes); // Protecting the Spotify routes

const port = process.env.PORT || 5000;
app.listen(port, () => console.log(`Server started on port ${port}`));

