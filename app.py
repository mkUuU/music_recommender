from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Spotify API credentials
client_id = 'your_client_id'
client_secret = 'your_client_secret'

# Get access token function
def get_spotify_access_token():
    auth_response = requests.post('https://accounts.spotify.com/api/token', 
                                  data={'grant_type': 'client_credentials'}, 
                                  auth=HTTPBasicAuth(client_id, client_secret))
    return auth_response.json()['access_token']

# Get user recommendations
@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    user_id = request.args.get('user_id')
    
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT title, artist 
            FROM songs 
            WHERE genre IN (
                SELECT favorite_genres FROM users WHERE user_id = %s
            ) OR artist IN (
                SELECT favorite_artists FROM users WHERE user_id = %s
            ) OR mood IN (
                SELECT preferred_moods FROM users WHERE user_id = %s
            )
        """, (user_id, user_id, user_id))
        
        recommendations = cursor.fetchall()
        return jsonify(recommendations)
    except Error as e:
        return jsonify({"error": str(e)})

# Add user profile
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    try:
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO users (name, favorite_genres, favorite_artists, preferred_moods) 
            VALUES (%s, %s, %s, %s)
        """, (data['name'], ','.join(data['favorite_genres']), ','.join(data['favorite_artists']), ','.join(data['preferred_moods'])))
        db.commit()
        return jsonify({'message': 'User added successfully'}), 201
    except Error as e:
        return jsonify({"error": str(e)})

# Search songs on Spotify
@app.route('/search_spotify', methods=['GET'])
def search_spotify():
    query = request.args.get('query')
    access_token = get_spotify_access_token()
    search_url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'q': query, 'type': 'track'}
    response = requests.get(search_url, headers=headers, params=params)
    
    songs = response.json()['tracks']['items']
    result = [{'title': song['name'], 'artist': song['artists'][0]['name']} for song in songs]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

