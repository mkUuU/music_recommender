import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MusicRecommendations = () => {
  const [mood, setMood] = useState('happy');
  const [recommendations, setRecommendations] = useState([]);

  const fetchRecommendations = async () => {
    const token = localStorage.getItem('token'); // Assuming Spotify token is stored
    const response = await axios.get(`http://localhost:5000/api/spotify/recommendations?mood=${mood}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    setRecommendations(response.data.tracks);
  };

  useEffect(() => {
    fetchRecommendations();
  }, [mood]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-3xl font-bold mb-6">Music Recommendations</h1>
      <select
        className="p-2 mb-6 border border-gray-300 rounded"
        onChange={(e) => setMood(e.target.value)}
      >
        <option value="happy">Happy</option>
        <option value="sad">Sad</option>
        <option value="energetic">Energetic</option>
      </select>

      <ul className="w-full max-w-2xl bg-white shadow-md rounded-lg p-6">
        {recommendations.map((track) => (
          <li key={track.id} className="mb-4">
            <p>{track.name} by {track.artists[0].name}</p>
            <audio controls src={track.preview_url} />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MusicRecommendations;

