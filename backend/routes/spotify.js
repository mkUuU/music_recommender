const express = require('express');
const axios = require('axios');

const router = express.Router();

// Get recommendations from Spotify
router.get('/recommendations', async (req, res) => {
  const { mood } = req.query;
  const spotifyToken = req.header('Authorization');

  try {
    const response = await axios.get('https://api.spotify.com/v1/recommendations', {
      headers: {
        'Authorization': `Bearer ${spotifyToken}`
      },
      params: {
        seed_genres: mood, // Use the mood to generate recommendations
        limit: 10
      }
    });
    
    res.send(response.data);
  } catch (error) {
    res.status(400).send('Error fetching recommendations');
  }
});

module.exports = router;

